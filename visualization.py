# visualization/visualization.py
import os
import sys
import argparse
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np
import pandas as pd
import joblib
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import torch
import umap
import warnings
from sklearn.model_selection import train_test_split

# 忽略警告
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# 设置中文字体支持
plt.rcParams['font.family'] = 'Microsoft YaHei'
plt.rcParams['axes.unicode_minus'] = False

def get_project_root():
    """获取项目根目录"""
    current_file = os.path.abspath(__file__)
    project_root = current_file
    while os.path.basename(project_root) != "Pytorch-Gan-based-dataset-expansion-main":
        project_root = os.path.dirname(project_root)
    return project_root

def calculate_kl_divergence(real_data, gen_data, bins=30, range=None):
    real_hist, bin_edges = np.histogram(real_data, bins=bins, density=True, range=range)
    gen_hist, _ = np.histogram(gen_data, bins=bin_edges, density=True)
    real_hist = real_hist + 1e-7
    gen_hist = gen_hist + 1e-7
    kl_divergence = np.sum(real_hist * np.log(real_hist / gen_hist))
    return kl_divergence

def calculate_js_divergence(real_data, gen_data, bins=30, range=None):
    real_hist, bin_edges = np.histogram(real_data, bins=bins, density=True, range=range)
    gen_hist, _ = np.histogram(gen_data, bins=bin_edges, density=True)
    real_hist = real_hist + 1e-7
    gen_hist = gen_hist + 1e-7
    m = (real_hist + gen_hist) / 2
    js_divergence = 0.5 * np.sum(real_hist * np.log(real_hist / m)) + 0.5 * np.sum(gen_hist * np.log(gen_hist / m))
    return js_divergence

def calculate_wasserstein_distance(real_data, gen_data):
    real_data = real_data.to(torch.float32)
    gen_data = gen_data.to(torch.float32)
    return torch.mean(real_data) - torch.mean(gen_data)

def visualize(building, floor, use_wgan=False, use_kpca=False, kpca_params=None):
    try:
        project_root = get_project_root()

        # 加载真实数据
        data_path = os.path.join(project_root, 'data', 'UJIndoorLoc', 'trainingData.csv')
        real_data = pd.read_csv(data_path)
        real_data = real_data[(real_data['BUILDINGID'] == building) & (real_data['FLOOR'] == floor)]

        if len(real_data) == 0:
            print(f"楼栋{building}楼层{floor}的真实数据为空，请检查数据集或选择其他楼栋和楼层。")
            return
    except Exception as e:
        print(f"加载真实数据失败: {e}")
        return

    # 加载生成数据
    gen_file_name = f"synthetic_data_{'wgan' if use_wgan else 'cgan'}_building_{building}_floor_{floor}.csv"
    gen_file_path = os.path.join(project_root, 'generated_samples', gen_file_name)
    if not os.path.exists(gen_file_path):
        print(f"生成数据文件不存在: {gen_file_path}")
        print("请先生成合成数据。")
        return

    try:
        gen_data = pd.read_csv(gen_file_path)
    except Exception as e:
        print(f"加载生成数据失败: {e}")
        return

    if gen_data.empty:
        print(f"生成数据文件 {gen_file_path} 为空")
        return

    print(f"真实数据维度: {real_data.shape}")
    print(f"生成数据维度: {gen_data.shape}")
    if real_data.shape[1] != gen_data.shape[1]:
        print("错误: 真实数据和生成数据的维度不匹配")
        return

    # 提取WAP特征列
    wap_columns = [f'WAP{i:03d}' for i in range(1, 521)]
    real_wap = real_data[wap_columns].values
    gen_wap = gen_data[wap_columns].values

    # 计算统计信息
    real_mean = np.mean(real_wap, axis=0)
    real_std = np.std(real_wap, axis=0)
    gen_mean = np.mean(gen_wap, axis=0)
    gen_std = np.std(gen_wap, axis=0)

    print("真实数据均值 (前5个特征):", real_mean[:5])
    print("生成数据均值 (前5个特征):", gen_mean[:5])
    print("真实数据标准差 (前5个特征):", real_std[:5])
    print("生成数据标准差 (前5个特征):", gen_std[:5])

    real_wap_flat = real_wap.flatten()
    gen_wap_flat = gen_wap.flatten()

    min_val = min(real_wap_flat.min(), gen_wap_flat.min())
    max_val = max(real_wap_flat.max(), gen_wap_flat.max())

    kl_divergence = calculate_kl_divergence(real_wap_flat, gen_wap_flat, range=(min_val, max_val))
    js_divergence = calculate_js_divergence(real_wap_flat, gen_wap_flat, range=(min_val, max_val))

    print(f"KL散度: {kl_divergence}")
    print(f"JS散度: {js_divergence}")

    real_tensor = torch.from_numpy(real_wap_flat).float()
    gen_tensor = torch.from_numpy(gen_wap_flat).float()
    wasserstein_distance = calculate_wasserstein_distance(real_tensor, gen_tensor)
    print(f"Wasserstein距离: {wasserstein_distance.item()}")

    try:
        # 使用逻辑回归分类器
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
        clf = LogisticRegression(max_iter=1000, class_weight='balanced')
        clf.fit(X_train_scaled, y_train)
        
        # 计算测试集准确率
        predictions = clf.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, predictions)
        print(f"平衡后分类准确率: {accuracy:.4f}")

    except Exception as e:
        print(f"计算分类准确率失败: {e}")

    try:
        wap_columns = [f'WAP{i:03d}' for i in range(1, 521)]
        real_wap = real_data[wap_columns].values
        gen_wap = gen_data[wap_columns].values

        combined = np.vstack([real_wap[:1000], gen_wap[:1000]])

        pca = PCA(n_components=2)
        pca_result = pca.fit_transform(combined)

        plt.figure(figsize=(10, 8))
        plt.scatter(pca_result[:1000, 0], pca_result[:1000, 1], alpha=0.5, label="真实数据")
        plt.scatter(pca_result[1000:, 0], pca_result[1000:, 1], alpha=0.5, label="生成数据")
        plt.title(f"楼栋{building}楼层{floor}数据分布对比 (PCA)")
        plt.legend()
        plt.axis('equal')

        save_dir = os.path.join(project_root, "visualization")
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, f"building_{building}_floor_{floor}_{'wgan' if use_wgan else 'cgan'}_pca.png")
        plt.savefig(save_path, format='png', dpi=300)
        plt.close()

        tsne = TSNE(n_components=2, random_state=42)
        tsne_result = tsne.fit_transform(combined)

        plt.figure(figsize=(10, 8))
        plt.scatter(tsne_result[:1000, 0], tsne_result[:1000, 1], alpha=0.5, label="真实数据")
        plt.scatter(tsne_result[1000:, 0], tsne_result[1000:, 1], alpha=0.5, label="生成数据")
        plt.title(f"楼栋{building}楼层{floor}数据分布对比 (t-SNE)")
        plt.legend()
        plt.axis('equal')

        save_path = os.path.join(save_dir, f"building_{building}_floor_{floor}_{'wgan' if use_wgan else 'cgan'}_tsne.png")
        plt.savefig(save_path, format='png', dpi=300)
        plt.close()

        umap_reducer = umap.UMAP()
        umap_result = umap_reducer.fit_transform(combined)

        plt.figure(figsize=(10, 8))
        plt.scatter(umap_result[:1000, 0], umap_result[:1000, 1], alpha=0.5, label="真实数据")
        plt.scatter(umap_result[1000:, 0], umap_result[:1000, 1], alpha=0.5, label="生成数据")
        plt.title(f"楼栋{building}楼层{floor}数据分布对比 (UMAP)")
        plt.legend()
        plt.axis('equal')

        save_path = os.path.join(save_dir, f"building_{building}_floor_{floor}_{'wgan' if use_wgan else 'cgan'}_umap.png")
        plt.savefig(save_path, format='png', dpi=300)
        plt.close()

    except Exception as e:
        print(f"可视化失败: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WiFi指纹数据集可视化")
    parser.add_argument("--building", type=int, required=True, help="目标楼ID")
    parser.add_argument("--floor", type=int, required=True, help="目标楼层ID")
    parser.add_argument("--use_wgan", type=int, default=1, help="是否使用 WGAN")
    parser.add_argument("--use_kpca", type=int, default=0, help="是否使用 kPCA")
    parser.add_argument("--kpca_d", type=int, default=3, help="kPCA 的维度")
    parser.add_argument("--kpca_type", type=str, default="rbf", help="kPCA 的核函数类型")
    parser.add_argument("--kpca_para", type=float, default=2, help="kPCA 的核函数参数")
    args = parser.parse_args()

    visualize(
        args.building, 
        args.floor, 
        use_wgan=bool(args.use_wgan), 
        use_kpca=bool(args.use_kpca), 
        kpca_params=(args.kpca_d, args.kpca_type, args.kpca_para) if args.use_kpca else None
    )