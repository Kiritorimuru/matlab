# clean_test_data.py
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib
import warnings

warnings.filterwarnings("ignore")

# 项目根目录
project_root = os.path.dirname(os.path.abspath(__file__))

def clean_dataset(df, building, floor):
    """统一的数据清洗函数（复用训练数据清洗逻辑）"""
    # 筛选指定楼栋楼层
    df = df[(df['BUILDINGID'] == building) & (df['FLOOR'] == floor)]
    if len(df) == 0:
        return None
    
    # 处理WAP列
    wap_columns = [f'WAP{i:03d}' for i in range(1, 521)]
    
    # 删除整列为100或标准差为0的列
    valid_wap_cols = []
    for col in wap_columns:
        if col in df.columns:
            # 删除全为100的列
            if (df[col] == 100).all():
                df.drop(col, axis=1, inplace=True)
                continue
            # 删除标准差为0的列
            if df[col].std() == 0:
                df.drop(col, axis=1, inplace=True)
                continue
            valid_wap_cols.append(col)
    
    # 处理小于-100的值
    df[valid_wap_cols] = df[valid_wap_cols].applymap(lambda x: np.nan if x < -100 else x)
    df.dropna(subset=valid_wap_cols, how='all', inplace=True)  # 仅当所有WAP值为空时删除
    
    return df[valid_wap_cols + ['BUILDINGID', 'FLOOR', 'LONGITUDE', 'LATITUDE']]

def process_test_data():
    # 读取测试数据
    test_path = os.path.join(project_root, "data", "UJIndoorLoc", "validationData.csv")
    test_df = pd.read_csv(test_path)
    
    # 创建保存目录
    save_dir = os.path.join(project_root, "test_data", "processed")
    os.makedirs(save_dir, exist_ok=True)
    
    # 获取所有楼栋-楼层组合
    buildings = test_df['BUILDINGID'].unique()
    floors = test_df['FLOOR'].unique()
    
    # 遍历每个楼栋-楼层组合
    for building in buildings:
        for floor in floors:
            # 清洗数据
            cleaned_df = clean_dataset(test_df.copy(), building, floor)
            if cleaned_df is None or len(cleaned_df) == 0:
                print(f"楼栋{building}楼层{floor}无测试数据")
                continue
            
            # 保存清洗后的数据
            save_path = os.path.join(save_dir, f"cleaned_test_building_{building}_floor_{floor}.csv")
            cleaned_df.to_csv(save_path, index=False)
            print(f"已保存测试数据：{save_path}")

if __name__ == "__main__":
    process_test_data()