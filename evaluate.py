# src/evaluate.py
import os
import sys
import torch
import numpy as np
import pandas as pd
import joblib
from model_arch import Generator
import argparse
import scipy.io

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

def generate_synthetic_data(num_samples, latent_dim=100, building=0, floor=0, use_kpca=False, kpca_params=None, use_wgan=False):
    try:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"使用的设备: {device}")

        saved_generator_path = os.path.join(project_root, "models", "final_generator.pth")
        if not os.path.exists(saved_generator_path):
            print("未找到生成器模型文件，请先训练模型。")
            return
        
        checkpoint = torch.load(saved_generator_path, map_location=device)
        output_dim = checkpoint['output_dim']
        
        generator = Generator(
            latent_dim=latent_dim,
            condition_dim=4,
            output_dim=output_dim
        )
        generator.load_state_dict(checkpoint['state_dict'])
        generator.to(device)
        generator.eval()

        scaler_rssi_path = os.path.join(project_root, "data", "processed", "scaler_rssi.pkl")
        scaler_location_path = os.path.join(project_root, "data", "processed", "scaler_location.pkl")
        scaler_rssi = joblib.load(scaler_rssi_path)
        scaler_location = joblib.load(scaler_location_path)

        processed_data_path = os.path.join(
            project_root, "data", "processed",
            f"cleaned_building_{building}_floor_{floor}.csv"
        )
        if not os.path.exists(processed_data_path):
            print(f"清洗后的数据文件 {processed_data_path} 不存在")
            return
        df_processed = pd.read_csv(processed_data_path)
        wap_columns = [col for col in df_processed.columns if col.startswith('WAP')]

        condition = torch.randn(num_samples, 4, device=device)
        z = torch.randn(num_samples, latent_dim, device=device)
        z_condition = torch.cat([z, condition], dim=1)
        with torch.no_grad():
            synthetic_data = generator(z_condition).cpu().numpy()

        synthetic_data_rssi = synthetic_data[:, :-2]
        synthetic_data_location = synthetic_data[:, -2:]
        synthetic_data_rssi = scaler_rssi.inverse_transform(synthetic_data_rssi)
        synthetic_data_location = scaler_location.inverse_transform(synthetic_data_location)

        if use_kpca:
            kpca_path = os.path.join(project_root, "data", "processed", "kpca_model.pkl")
            kpca = joblib.load(kpca_path)
            synthetic_data_rssi = kpca.inverse_transform(synthetic_data_rssi)

        synthetic_data_rssi = np.where(
            (synthetic_data_rssi > 0) & (synthetic_data_rssi != 100), 
            100, 
            synthetic_data_rssi
        )

        synthetic_df = pd.DataFrame(synthetic_data_rssi, columns=wap_columns)
        synthetic_df[['LONGITUDE', 'LATITUDE']] = synthetic_data_location

        generated_data_dir = os.path.join(project_root, "generated_samples")
        os.makedirs(generated_data_dir, exist_ok=True)
        gen_file_name = f"synthetic_data_{'wgan' if use_wgan else 'cgan'}_building_{building}_floor_{floor}.csv"
        generated_data_path = os.path.join(generated_data_dir, gen_file_name)
        synthetic_df.to_csv(generated_data_path, index=False)

        generated_mat_path = os.path.join(generated_data_dir, gen_file_name.replace('.csv', '.mat'))
        scipy.io.savemat(generated_mat_path, {
            'RSS': synthetic_data_rssi,
            'LOC': synthetic_data_location
        })

        print(f"生成的数据已保存到 {generated_data_path}")
        return synthetic_df

    except Exception as e:
        print(f"生成数据失败: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="生成指定楼和楼层的合成数据")
    parser.add_argument("--num_samples", type=int, default=1000, help="生成的样本数量")
    parser.add_argument("--building", type=int, default=0, help="指定楼ID")
    parser.add_argument("--floor", type=int, default=0, help="指定楼层ID")
    parser.add_argument("--use_kpca", type=int, default=0, help="是否使用 kPCA")
    parser.add_argument("--kpca_d", type=int, default=3, help="kPCA 的维度")
    parser.add_argument("--kpca_type", type=str, default="rbf", help="kPCA 的核函数类型")
    parser.add_argument("--kpca_para", type=float, default=2, help="kPCA 的核函数参数")
    parser.add_argument("--use_wgan", type=int, default=1, help="是否使用 WGAN")
    args = parser.parse_args()

    generate_synthetic_data(
        args.num_samples,
        building=args.building,
        floor=args.floor,
        use_kpca=bool(args.use_kpca),
        kpca_params=(args.kpca_d, args.kpca_type, args.kpca_para),
        use_wgan=bool(args.use_wgan)
    )