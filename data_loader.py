# src/data_loader.py
import os
import sys
import pandas as pd
import numpy as np
import torch
from torch.utils.data import DataLoader, TensorDataset
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import KernelPCA
import warnings
import argparse

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

def load_and_preprocess(data_path, building=None, floor=None, use_kpca=False, kpca_params=None):
    if not os.path.exists(data_path):
        print(f"数据文件 {data_path} 不存在")
        return None, None

    df = pd.read_csv(data_path)

    if building is not None:
        df = df[df['BUILDINGID'] == building]
    if floor is not None:
        df = df[df['FLOOR'] == floor]

    if len(df) == 0:
        print(f"楼栋 {building} 楼层 {floor} 的数据为空")
        return None, None

    wap_columns = [f'WAP{i:03d}' for i in range(1, 521)]
    
    # 剔除整列值为100或标准差为0的列
    for col in wap_columns:
        if col in df.columns:
            if (df[col] == 100).all() or df[col].std() == 0:
                df.drop(col, axis=1, inplace=True)
                
    wap_columns = [col for col in wap_columns if col in df.columns]
    
    # 处理小于-100的值
    df[wap_columns] = df[wap_columns].applymap(lambda x: np.nan if x < -100 else x)
    df.dropna(subset=wap_columns, inplace=True)

    # 保存清洗后的数据
    processed_data_dir = os.path.join(project_root, "data", "processed")
    os.makedirs(processed_data_dir, exist_ok=True)
    cleaned_path = os.path.join(processed_data_dir, f"cleaned_building_{building}_floor_{floor}.csv")
    df.to_csv(cleaned_path, index=False)
    print(f"清洗后的数据已保存到 {cleaned_path}")

    # 标准化
    scaler_rssi = StandardScaler()
    X_rssi_scaled = scaler_rssi.fit_transform(df[wap_columns].values)
    joblib.dump(scaler_rssi, os.path.join(project_root, "data", "processed", "scaler_rssi.pkl"))

    scaler_location = StandardScaler()
    X_location_scaled = scaler_location.fit_transform(df[['LONGITUDE', 'LATITUDE']].values)
    joblib.dump(scaler_location, os.path.join(project_root, "data", "processed", "scaler_location.pkl"))

    X = np.hstack([X_rssi_scaled, X_location_scaled])

    if use_kpca and kpca_params:
        kpca = KernelPCA(n_components=kpca_params[0], kernel=kpca_params[1], gamma=kpca_params[2])
        X = kpca.fit_transform(X)
        joblib.dump(kpca, os.path.join(project_root, "data", "processed", "kpca_model.pkl"))

    tensor_X = torch.FloatTensor(X)
    dataset = TensorDataset(tensor_X)
    loader = DataLoader(dataset, batch_size=64, shuffle=True)
    print(f"已加载 {len(df)} 条数据 (楼栋 {building}, 楼层 {floor})")
    print(f"输入维度: {X.shape[1]}")
    return loader, X.shape[1]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="数据预处理")
    parser.add_argument("--building", type=int, required=True, help="目标楼ID")
    parser.add_argument("--floor", type=int, required=True, help="目标楼层ID")
    parser.add_argument("--use_kpca", type=int, default=0, help="是否使用 kPCA")
    parser.add_argument("--kpca_d", type=int, default=3, help="kPCA 的维度")
    parser.add_argument("--kpca_type", type=str, default="rbf", help="kPCA 的核函数类型")
    parser.add_argument("--kpca_para", type=float, default=2, help="kPCA 的核函数参数")
    args = parser.parse_args()

    load_and_preprocess(
        data_path=os.path.join(project_root, "data", "UJIndoorLoc", "trainingData.csv"),
        building=args.building,
        floor=args.floor,
        use_kpca=bool(args.use_kpca),
        kpca_params=(args.kpca_d, args.kpca_type, args.kpca_para)
    )