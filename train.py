# src/train.py
import os
import sys
import torch
import torch.nn as nn
import torch.optim as optim
from torch.cuda.amp import autocast, GradScaler
import time
import numpy as np
from model_arch import Generator, Discriminator
from data_loader import load_and_preprocess
import argparse
from torch.optim.lr_scheduler import CosineAnnealingLR

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class Config:
    latent_dim = 100
    condition_dim = 4
    epochs = 7000
    batch_size = 64
    lr = 0.00003
    save_interval = 300
    log_interval = 50

def init_models(input_dim):
    generator = Generator(
        latent_dim=Config.latent_dim,
        condition_dim=Config.condition_dim,
        output_dim=input_dim
    )
    discriminator = Discriminator(
        input_dim=input_dim,
        condition_dim=Config.condition_dim
    )
    generator.to(device)
    discriminator.to(device)
    return generator, discriminator

def gradient_penalty(D, real_data, fake_data, condition, lambda_gp=10.0):
    batch_size = real_data.size(0)
    alpha = torch.rand(batch_size, 1).expand_as(real_data).to(real_data.device)
    interpolated = alpha * real_data + (1 - alpha) * fake_data
    interpolated = interpolated.detach().requires_grad_(True)
    D_interpolated = D(interpolated, condition)
    gradients = torch.autograd.grad(
        outputs=D_interpolated,
        inputs=interpolated,
        grad_outputs=torch.ones(D_interpolated.size()).to(real_data.device),
        create_graph=True,
        retain_graph=True
    )[0]
    gradient_penalty = ((gradients.norm(2, dim=1) - 1) ** 2).mean() * lambda_gp
    return gradient_penalty

def train(building, floor, use_kpca=False, kpca_params=None, use_wgan_gp=True, lambda_gp=10.0, lambda_physical=0.03, epochs=7000, lr=0.00003):
    try:
        data_path = os.path.join(project_root, "data", "UJIndoorLoc", "trainingData.csv")
        data_loader, input_dim = load_and_preprocess(data_path, building, floor, use_kpca, kpca_params)
        if data_loader is None:
            return
        print(f"\n[数据加载] 批次数: {len(data_loader)} | 输入维度: {input_dim}")

        generator, discriminator = init_models(input_dim)
        
        optimizer_G = optim.Adam(generator.parameters(), lr=lr, betas=(0.5, 0.999))
        optimizer_D = optim.Adam(discriminator.parameters(), lr=lr, betas=(0.5, 0.999))
        
        scheduler_G = CosineAnnealingLR(optimizer_G, T_max=1000)
        scheduler_D = CosineAnnealingLR(optimizer_D, T_max=1000)
        
        scaler = GradScaler()
        history = {'D_loss': [], 'G_loss': [], 'Wasserstein_distance': []}
        
        print(f"\n[训练启动] 设备: {device}")
        start_time = time.time()

        for epoch in range(epochs):
            for i, real_data in enumerate(data_loader):
                real_data = real_data[0].to(device, non_blocking=True)
                batch_size = real_data.size(0)
                condition = torch.randn(batch_size, Config.condition_dim, device=device)
                
                optimizer_D.zero_grad(set_to_none=True)
                with autocast():
                    real_validity = discriminator(real_data, condition)
                    z = torch.randn(batch_size, Config.latent_dim, device=device)
                    z_condition = torch.cat([z, condition], dim=1)
                    fake_data = generator(z_condition)
                    fake_validity = discriminator(fake_data.detach(), condition)
                    wasserstein_distance = torch.mean(real_validity) - torch.mean(fake_validity)
                    gp = gradient_penalty(discriminator, real_data, fake_data, condition, lambda_gp)
                    d_loss = -wasserstein_distance + gp
                    p_loss = torch.relu(-100 - fake_data).mean() * lambda_physical
                    d_loss += p_loss
                
                scaler.scale(d_loss).backward()
                scaler.step(optimizer_D)
                
                if i % 5 == 0:
                    optimizer_G.zero_grad(set_to_none=True)
                    with autocast():
                        z = torch.randn(batch_size, Config.latent_dim, device=device)
                        z_condition = torch.cat([z, condition], dim=1)
                        fake_data = generator(z_condition)
                        fake_validity = discriminator(fake_data, condition)
                        g_loss = -torch.mean(fake_validity)
                    scaler.scale(g_loss).backward()
                    scaler.step(optimizer_G)
                
                scaler.update()
                
                history['D_loss'].append(d_loss.item())
                history['G_loss'].append(g_loss.item() if i % 5 == 0 else 0)
                history['Wasserstein_distance'].append(wasserstein_distance.item())

            scheduler_G.step()
            scheduler_D.step()

            if (epoch + 1) % Config.log_interval == 0:
                avg_d_loss = np.mean(history['D_loss'][-len(data_loader):])
                avg_g_loss = np.mean([loss for i, loss in enumerate(history['G_loss'][-len(data_loader):]) if i % 5 == 0])
                avg_wasserstein = np.mean(history['Wasserstein_distance'][-len(data_loader):])
                print(f"Epoch [{epoch+1}/{epochs}] D_loss: {avg_d_loss:.4f} G_loss: {avg_g_loss:.4f} Wasserstein: {avg_wasserstein:.4f} Time: {time.time()-start_time:.2f}s")

            if (epoch + 1) % Config.save_interval == 0:
                save_dir = os.path.join(project_root, "models")
                os.makedirs(save_dir, exist_ok=True)
                torch.save({
                    'state_dict': generator.state_dict(),
                    'output_dim': input_dim
                }, os.path.join(save_dir, f"generator_epoch{epoch+1}.pth"))
                print(f"[模型保存] 已保存周期 {epoch+1} 的模型到 {save_dir}/")

        print(f"\n[训练完成] 总耗时: {(time.time()-start_time)/60:.2f}分钟")
        torch.save({
            'state_dict': generator.state_dict(),
            'output_dim': input_dim
        }, os.path.join(project_root, "models", "final_generator.pth"))

    except Exception as e:
        print(f"\n[训练失败] {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="训练指定楼和楼层的 WGAN-GP 模型")
    parser.add_argument("--building", type=int, default=0, help="指定楼ID")
    parser.add_argument("--floor", type=int, default=0, help="指定楼层ID")
    parser.add_argument("--use_kpca", type=int, default=0, help="是否使用 kPCA")
    parser.add_argument("--kpca_d", type=int, default=3, help="kPCA 的维度")
    parser.add_argument("--kpca_type", type=str, default="rbf", help="kPCA 的核函数类型")
    parser.add_argument("--kpca_para", type=float, default=2, help="kPCA 的核函数参数")
    parser.add_argument("--use_wgan", type=int, default=1, help="是否使用 WGAN")
    parser.add_argument("--lambda_gp", type=float, default=10.0, help="梯度惩罚系数λ_gp")
    parser.add_argument("--lambda_physical", type=float, default=0.03, help="物理约束系数λ_physical")
    parser.add_argument("--epochs", type=int, default=7000, help="训练次数")
    parser.add_argument("--lr", type=float, default=0.00003, help="学习率")
    args = parser.parse_args()

    train(
        building=args.building,
        floor=args.floor,
        use_kpca=bool(args.use_kpca),
        kpca_params=(args.kpca_d, args.kpca_type, args.kpca_para),
        use_wgan_gp=bool(args.use_wgan),
        lambda_gp=args.lambda_gp,
        lambda_physical=args.lambda_physical,
        epochs=args.epochs,
        lr=args.lr
    )