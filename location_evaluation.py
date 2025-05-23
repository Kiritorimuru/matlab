# src/location_evaluation.py
import argparse
import os
import sys
import numpy as np
import pandas as pd
import joblib
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
import warnings
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.ensemble import VotingRegressor
from sklearn.feature_selection import SelectKBest, f_regression

# 忽略警告
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

def get_project_root():
    """获取项目根目录"""
    current_file = os.path.abspath(__file__)
    project_root = current_file
    while os.path.basename(project_root) != "Pytorch-Gan-based-dataset-expansion-main":
        project_root = os.path.dirname(project_root)
    return project_root

def wknn_predict(rss_test, fp_rss, fp_loc, k=3):
    # 计算测试点与所有指纹点的距离
    distances = cdist(rss_test, fp_rss, metric='euclidean')
    
    # 获取最近的k个点的索引
    indices = np.argsort(distances, axis=1)[:, :k]
    
    # 计算加权平均位置
    weights = 1.0 / (distances[np.arange(len(rss_test))[:, None], indices] + 1e-5)
    weights /= np.sum(weights, axis=1, keepdims=True)
    
    predictions = np.zeros((len(rss_test), 2))
    for i in range(len(rss_test)):
        predictions[i] = np.sum(fp_loc[indices[i]] * weights[i].reshape(-1, 1), axis=0)
    
    return predictions

def calculate_position_error(X_train, y_train, X_test, y_test, k=3):
    # 提取坐标信息
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # 使用WKNN预测
    predictions = wknn_predict(X_test_scaled, X_train_scaled, y_train, k=k)
    
    # 计算平均定位误差
    error = np.mean(np.sqrt(np.sum((predictions - y_test)**2, axis=1)))
    return error

def evaluate_classifiers(real_wap, gen_wap, real_coords, gen_coords):
    # 合并数据
    X_real = real_wap
    X_gen = gen_wap
    y_real = real_coords
    y_gen = gen_coords

    # 平衡数据集
    min_samples = min(len(X_real), len(X_gen))
    X_balanced = np.vstack([X_real[:min_samples], X_gen[:min_samples]])
    y_balanced = np.vstack([y_real[:min_samples], y_gen[:min_samples]])

    # 划分训练测试集
    X_train, X_test, y_train, y_test = train_test_split(X_balanced, y_balanced, test_size=0.3)

    # 数据标准化
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 特征选择
    selector = SelectKBest(f_regression, k=100)  # 选择100个最重要的特征
    X_train_selected = selector.fit_transform(X_train_scaled, y_train[:, 0])  # 确保 y 是一维数组
    X_test_selected = selector.transform(X_test_scaled)

    # K最近邻 (WKNN)
    wknn_error = calculate_position_error(X_train_selected, y_train, X_test_selected, y_test, k=3)
    print(f"K最近邻 (WKNN) 平均定位误差: {wknn_error:.2f} 米")

    # 随机森林回归（分别处理两个坐标维度）
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train_selected, y_train[:, 0])  # 训练经度预测
    rf_predictions_lon = rf.predict(X_test_selected)
    rf.fit(X_train_selected, y_train[:, 1])  # 训练纬度预测
    rf_predictions_lat = rf.predict(X_test_selected)
    rf_error = np.mean(np.sqrt((rf_predictions_lon - y_test[:, 0])**2 + (rf_predictions_lat - y_test[:, 1])**2))
    print(f"随机森林回归平均定位误差: {rf_error:.2f} 米")

    # 支持向量机（分别处理两个坐标维度）
    svm = SVR(kernel='rbf', C=1.0, gamma='scale')
    svm.fit(X_train_selected, y_train[:, 0])  # 训练经度预测
    svm_predictions_lon = svm.predict(X_test_selected)
    svm.fit(X_train_selected, y_train[:, 1])  # 训练纬度预测
    svm_predictions_lat = svm.predict(X_test_selected)
    svm_error = np.mean(np.sqrt((svm_predictions_lon - y_test[:, 0])**2 + (svm_predictions_lat - y_test[:, 1])**2))
    print(f"支持向量机平均定位误差: {svm_error:.2f} 米")

    # 集成学习 - 投票回归器（分别处理两个坐标维度）
    estimators = [
        ('rf', rf),
        ('svm', svm)
    ]
    vr_lon = VotingRegressor(estimators)
    vr_lon.fit(X_train_selected, y_train[:, 0])  # 训练经度预测
    vr_lat = VotingRegressor(estimators)
    vr_lat.fit(X_train_selected, y_train[:, 1])  # 训练纬度预测
    vr_predictions_lon = vr_lon.predict(X_test_selected)
    vr_predictions_lat = vr_lat.predict(X_test_selected)
    vr_error = np.mean(np.sqrt((vr_predictions_lon - y_test[:, 0])**2 + (vr_predictions_lat - y_test[:, 1])**2))
    print(f"集成学习平均定位误差: {vr_error:.2f} 米")

def evaluate_location(building, floor, use_wgan=False, use_kpca=False, kpca_params=None):
    try:
        project_root = get_project_root()

        # 加载真实数据（训练集）
        train_data_path = os.path.join(project_root, 'data', 'UJIndoorLoc', 'trainingData.csv')
        real_data = pd.read_csv(train_data_path)
        real_data = real_data[(real_data['BUILDINGID'] == building) & (real_data['FLOOR'] == floor)]

        # 加载验证集
        val_data_path = os.path.join(project_root, 'data', 'UJIndoorLoc', 'validationData.csv')
        val_data = pd.read_csv(val_data_path)
        val_data = val_data[(val_data['BUILDINGID'] == building) & (val_data['FLOOR'] == floor)]

        if len(real_data) == 0 or len(val_data) == 0:
            print(f"楼栋{building}楼层{floor}的数据为空，请检查数据集或选择其他楼栋和楼层。")
            return
    except Exception as e:
        print(f"加载数据失败: {e}")
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
    print(f"验证数据维度: {val_data.shape}")
    print(f"生成数据维度: {gen_data.shape}")
    if real_data.shape[1] != gen_data.shape[1] or val_data.shape[1] != gen_data.shape[1]:
        print("错误: 数据集维度不匹配")
        return

    # 提取WAP特征列
    wap_columns = [f'WAP{i:03d}' for i in range(1, 521)]
    real_wap = real_data[wap_columns].values
    val_wap = val_data[wap_columns].values
    gen_wap = gen_data[wap_columns].values

    # 提取位置信息
    real_coords = real_data[['LONGITUDE', 'LATITUDE']].values
    gen_coords = gen_data[['LONGITUDE', 'LATITUDE']].values
    val_coords = val_data[['LONGITUDE', 'LATITUDE']].values

    # 合并数据并划分训练测试集
    X = np.vstack([real_wap, gen_wap])
    y = np.vstack([real_coords, gen_coords])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

    # 调整WKNN的k值选择范围
    best_k = 1
    best_error = float('inf')
    for k in range(1, 15):  # 扩大k值的选择范围
        position_error = calculate_position_error(X_train, y_train, X_test, y_test, k=k)
        print(f"k={k}: 平均定位误差: {position_error:.2f} 米")
        if position_error < best_error:
            best_error = position_error
            best_k = k

    print(f"最佳k值: {best_k}, 最佳平均定位误差: {best_error:.2f} 米")

    # 数据混合实验（调整混合比例）
    mix_ratios = [0.7, 0.5, 0.3]  # 调整生成数据占比
    for ratio in mix_ratios:
        num_real = int(len(real_wap) * (1 - ratio))
        num_gen = int(len(gen_wap) * ratio)
        X_mixed = np.vstack([real_wap[:num_real], gen_wap[:num_gen]])
        y_mixed = np.vstack([real_coords[:num_real], gen_coords[:num_gen]])
        
        X_train, X_test, y_train, y_test = train_test_split(X_mixed, y_mixed, test_size=0.3)
        error = calculate_position_error(X_train, y_train, X_test, y_test, k=best_k)
        print(f"混合比例 {ratio}: 平均误差 {error:.2f} 米")

    # 评估多种机器学习算法
    evaluate_classifiers(real_wap, gen_wap, real_coords, gen_coords)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WiFi指纹数据集定位验证")
    parser.add_argument("--building", type=int, required=True, help="目标楼ID")
    parser.add_argument("--floor", type=int, required=True, help="目标楼层ID")
    parser.add_argument("--use_wgan", type=int, default=1, help="是否使用 WGAN")
    parser.add_argument("--use_kpca", type=int, default=0, help="是否使用 kPCA")
    parser.add_argument("--kpca_d", type=int, default=3, help="kPCA 的维度")
    parser.add_argument("--kpca_type", type=str, default="rbf", help="kPCA 的核函数类型")
    parser.add_argument("--kpca_para", type=float, default=2, help="kPCA 的核函数参数")
    args = parser.parse_args()

    evaluate_location(
        args.building, 
        args.floor, 
        use_wgan=bool(args.use_wgan), 
        use_kpca=bool(args.use_kpca), 
        kpca_params=(args.kpca_d, args.kpca_type, args.kpca_para) if args.use_kpca else None
    )