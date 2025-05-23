# main.py
import argparse
import subprocess
import sys
from pathlib import Path
import os
import torch
import pandas as pd
from src.data_loader import load_and_preprocess
import warnings

# 禁用 TensorFlow 的日志输出
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# 忽略警告
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

def check_dependencies():
    try:
        import torch, pandas, joblib, numpy, matplotlib, sklearn
    except ImportError as e:
        print(f"缺少依赖: {e}")
        sys.exit(1)

def run_preprocess(building, floor, use_kpca=False, kpca_params=None):
    print(f"\n=== 预处理楼栋{building}楼层{floor}数据 ===")
    cmd = [
        "python", os.path.join("src", "data_loader.py"),
        "--building", str(building),
        "--floor", str(floor),
        "--use_kpca", str(int(use_kpca))
    ]
    if use_kpca:
        d, kpca_type, kpca_para = kpca_params
        cmd.extend(["--kpca_d", str(d), "--kpca_type", kpca_type, "--kpca_para", str(kpca_para)])
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"预处理失败: {e}")
        return False

def run_training(building, floor, use_kpca=False, kpca_params=None, use_wgan=False, lambda_gp=18.0, lambda_physical=0.03, lr=0.00003, epochs=7000):
    print(f"\n=== 训练楼栋{building}楼层{floor}模型 ===")
    cmd = [
        "python", os.path.join("src", "train.py"),
        "--building", str(building),
        "--floor", str(floor),
        "--use_wgan", str(int(use_wgan)),
        "--lambda_gp", str(lambda_gp),
        "--lambda_physical", str(lambda_physical),
        "--lr", str(lr),
        "--epochs", str(epochs)
    ]
    if use_kpca and kpca_params:
        d, kpca_type, kpca_para = kpca_params
        cmd.extend(["--use_kpca", "1", "--kpca_d", str(d), "--kpca_type", kpca_type, "--kpca_para", str(kpca_para)])
    else:
        cmd.extend(["--use_kpca", "0"])
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"训练失败: {e}")
        return False

def run_generation(building, floor, num_samples=1000, use_kpca=False, kpca_params=None, use_wgan=False):
    print(f"\n=== 生成楼栋{building}楼层{floor}数据 ===")
    cmd = [
        "python", os.path.join("src", "evaluate.py"),
        "--building", str(building),
        "--floor", str(floor),
        "--num_samples", str(num_samples),
        "--use_wgan", str(int(use_wgan))
    ]
    if use_kpca and kpca_params:
        d, kpca_type, kpca_para = kpca_params
        cmd.extend(["--use_kpca", "1", "--kpca_d", str(d), "--kpca_type", kpca_type, "--kpca_para", str(kpca_para)])
    else:
        cmd.extend(["--use_kpca", "0"])
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"生成失败: {e}")
        return False

def run_visualization(building, floor, use_wgan=False, use_kpca=False, kpca_params=None):
    print(f"\n=== 可视化楼栋{building}楼层{floor}数据 ===")
    try:
        visualization_script_path = os.path.join("visualization", "visualization.py")
        cmd = [
            "python", visualization_script_path,
            "--building", str(building),
            "--floor", str(floor),
            "--use_wgan", str(int(use_wgan)),
            "--use_kpca", str(int(use_kpca))
        ]
        if use_kpca and kpca_params:
            d, kpca_type, kpca_para = kpca_params
            cmd.extend(["--kpca_d", str(d), "--kpca_type", kpca_type, "--kpca_para", str(kpca_para)])
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"可视化失败: {e}")
        return False

def run_location_evaluation(building, floor, use_wgan=False, use_kpca=False, kpca_params=None):
    print(f"\n=== 定位验证楼栋{building}楼层{floor}数据 ===")
    try:
        location_evaluation_script_path = os.path.join("src", "location_evaluation.py")
        cmd = [
            "python", location_evaluation_script_path,
            "--building", str(building),
            "--floor", str(floor),
            "--use_wgan", str(int(use_wgan)),
            "--use_kpca", str(int(use_kpca))
        ]
        if use_kpca and kpca_params:
            d, kpca_type, kpca_para = kpca_params
            cmd.extend(["--kpca_d", str(d), "--kpca_type", kpca_type, "--kpca_para", str(kpca_para)])
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"定位验证失败: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="WiFi指纹数据集扩充系统")
    parser.add_argument("--building", type=int, required=True, help="目标楼ID")
    parser.add_argument("--floor", type=int, required=True, help="目标楼层ID")
    parser.add_argument("--num_samples", type=int, default=1000, help="生成的样本数量")
    parser.add_argument("--all", action="store_true", help="执行完整流程")
    parser.add_argument("--preprocess", action="store_true", help="仅执行数据预处理")
    parser.add_argument("--train", action="store_true", help="仅执行模型训练")
    parser.add_argument("--generate", action="store_true", help="仅执行数据生成")
    parser.add_argument("--visualize", action="store_true", help="仅执行数据可视化")
    parser.add_argument("--location_eval", action="store_true", help="仅执行定位验证")
    parser.add_argument("--use_kpca", type=int, default=0, help="是否使用 kPCA")
    parser.add_argument("--kpca_d", type=int, default=3, help="kPCA 的维度")
    parser.add_argument("--kpca_type", type=str, default="rbf", help="kPCA 的核函数类型")
    parser.add_argument("--kpca_para", type=float, default=2, help="kPCA 的核函数参数")
    parser.add_argument("--use_wgan", type=int, default=1, help="是否使用 WGAN")
    parser.add_argument("--lambda_gp", type=float, default=18.0, help="梯度惩罚系数λ")
    parser.add_argument("--lambda_physical", type=float, default=0.03, help="物理约束系数λ_physical")
    parser.add_argument("--lr", type=float, default=0.00003, help="学习率")
    parser.add_argument("--epochs", type=int, default=7000, help="训练周期")
    args = parser.parse_args()
    
    check_dependencies()
    
    use_kpca = bool(args.use_kpca)
    kpca_params = (args.kpca_d, args.kpca_type, args.kpca_para) if use_kpca else None
    use_wgan = bool(args.use_wgan)
    
    success = True
    if args.all or args.preprocess:
        success &= run_preprocess(args.building, args.floor, use_kpca, kpca_params)
    
    if args.all or args.train:
        success &= run_training(
            args.building, 
            args.floor, 
            use_kpca, 
            kpca_params, 
            use_wgan, 
            args.lambda_gp, 
            args.lambda_physical,
            args.lr,
            args.epochs
        )
    
    if args.all or args.generate:
        success &= run_generation(args.building, args.floor, args.num_samples, use_kpca, kpca_params, use_wgan)
    
    if args.all or args.visualize:
        success &= run_visualization(args.building, args.floor, use_wgan, use_kpca, kpca_params)
    
    if args.all or args.location_eval:
        success &= run_location_evaluation(args.building, args.floor, use_wgan, use_kpca, kpca_params)
    
    print("\n=== 执行结果 ===")
    print("成功" if success else "部分步骤失败")

if __name__ == "__main__":
    main()
