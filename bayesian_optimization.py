# src/bayesian_optimization.py
import os
import sys
import warnings
import numpy as np
import optuna
from sklearn.discriminant_analysis import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import torch
from train import train  # 确保正确导入训练函数
from evaluate import calculate_kl_divergence, calculate_js_divergence  # 确保正确导入评估指标
import pandas as pd
from data_loader import load_and_preprocess
import argparse
from evaluate import generate_synthetic_data
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB  # 导入 GaussianNB

# 添加项目根目录到 sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# 忽略警告
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

def objective(trial, args):
    # 超参数搜索空间
    lambda_gp = trial.suggest_float('lambda_gp', 10, 20)  # 进一步扩大lambda_gp的搜索范围
    lambda_physical = trial.suggest_float('lambda_physical', 0.001, 0.05)  # 进一步缩小lambda_physical的搜索范围
    lr = trial.suggest_float('lr', 1e-5, 1e-4, log=True)  # 调整学习率范围

    # 训练模型
    train_results = train(
        building=args.building,
        floor=args.floor,
        use_kpca=args.use_kpca,
        kpca_params=args.kpca_params,
        use_wgan=args.use_wgan,
        lambda_gp=lambda_gp,
        lambda_physical=lambda_physical,
        epochs=5000,  # 使用固定训练次数
        lr=lr
    )

    # 加载生成数据和真实数据
    real_data_path = os.path.join(project_root, "data", "UJIndoorLoc", "trainingData.csv")
    real_data = pd.read_csv(real_data_path)

    gen_file_name = f"synthetic_data_{'wgan' if args.use_wgan else 'cgan'}_building_{args.building}_floor_{args.floor}.csv"
    gen_data_path = os.path.join(project_root, "generated_samples", gen_file_name)
    gen_data = pd.read_csv(gen_data_path)

    if gen_data.empty:
        print(f"生成数据文件 {gen_file_name} 为空")
        return float('inf')  # 返回一个很大的值，表示失败

    # 筛选指定楼栋和楼层的数据
    real_data = real_data[(real_data['BUILDINGID'] == args.building) & (real_data['FLOOR'] == args.floor)]
    gen_data = gen_data[(gen_data['BUILDINGID'] == args.building) & (gen_data['FLOOR'] == args.floor)]

    if len(real_data) == 0 or len(gen_data) == 0:
        print("数据为空，请检查楼栋和楼层参数。")
        return float('inf')  # 返回一个很大的值，表示失败

    # 提取WAP特征列
    wap_columns = [f'WAP{i:03d}' for i in range(1, 521)]
    real_wap = real_data[wap_columns].values
    gen_wap = gen_data[wap_columns].values

    # 计算评估指标
    kl_divergence = calculate_kl_divergence(real_wap.flatten(), gen_wap.flatten())
    js_divergence = calculate_js_divergence(real_wap.flatten(), gen_wap.flatten())

    # 计算分类准确率
    X_real = real_wap
    X_gen = gen_wap
    y_real = np.ones(len(X_real))
    y_gen = np.zeros(len(X_gen))

    # 平衡数据集
    min_samples = min(len(X_real), len(X_gen))
    X_balanced = np.vstack([X_real[:min_samples], X_gen[:min_samples]])
    y_balanced = np.hstack([y_real[:min_samples], y_gen[:min_samples]])

    # 划分训练测试集
    X_train, X_test, y_train, y_test = train_test_split(X_balanced, y_balanced, test_size=0.3, stratify=y_balanced)

    # 数据标准化
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 使用逻辑回归分类器
    clf_lr = LogisticRegression(max_iter=1000, class_weight='balanced')
    clf_lr.fit(X_train_scaled, y_train)
    predictions_lr = clf_lr.predict(X_test_scaled)
    accuracy_lr = accuracy_score(y_test, predictions_lr)

    # 使用朴素贝叶斯分类器
    clf_nb = GaussianNB()
    clf_nb.fit(X_train_scaled, y_train)
    predictions_nb = clf_nb.predict(X_test_scaled)
    accuracy_nb = accuracy_score(y_test, predictions_nb)

    # 返回分类准确率的负值，因为我们要最小化分类准确率
    return -(accuracy_lr + accuracy_nb) / 2  # 返回两个分类器准确率的平均值

def main():
    parser = argparse.ArgumentParser(description="贝叶斯优化超参数")
    parser.add_argument("--building", type=int, required=True, help="目标楼ID")
    parser.add_argument("--floor", type=int, required=True, help="目标楼层ID")
    parser.add_argument("--use_kpca", type=int, default=0, help="是否使用 kPCA")
    parser.add_argument("--kpca_d", type=int, default=3, help="kPCA 的维度")
    parser.add_argument("--kpca_type", type=str, default="rbf", help="kPCA 的核函数类型")
    parser.add_argument("--kpca_para", type=float, default=2, help="kPCA 的核函数参数")
    parser.add_argument("--use_wgan", type=int, default=1, help="是否使用 WGAN")
    parser.add_argument("--n_trials", type=int, default=50, help="贝叶斯优化的试验次数")
    args = parser.parse_args()

    args.kpca_params = (args.kpca_d, args.kpca_type, args.kpca_para) if args.use_kpca else None
    args.use_wgan = bool(args.use_wgan)

    study = optuna.create_study(direction='minimize')
    study.optimize(lambda trial: objective(trial, args), n_trials=args.n_trials)

    print("最佳超参数:")
    print(f"lambda_gp: {study.best_trial.params['lambda_gp']}")
    print(f"lambda_physical: {study.best_trial.params['lambda_physical']}")
    print(f"学习率: {study.best_trial.params['lr']}")
    print(f"最佳分类准确率: {-study.best_value}")

if __name__ == "__main__":
    main()