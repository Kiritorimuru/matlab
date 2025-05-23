# merge_datasets.py
import os
import pandas as pd
import numpy as np
import scipy.io
import warnings

warnings.filterwarnings("ignore")

# 项目根目录
project_root = os.path.dirname(os.path.abspath(__file__))

def process_and_merge_data(building, floor):
    """处理并合并指定楼层的训练和测试数据"""
    print(f"\n=== 正在处理楼栋{building}楼层{floor} ===")
    
    # ============================== 1. 加载数据 ==============================
    # 加载清洗后的训练数据
    train_path = os.path.join(
        project_root, "data", "processed",
        f"cleaned_building_{building}_floor_{floor}.csv"
    )
    try:
        train_df = pd.read_csv(train_path)
        print(f"成功加载训练数据：{train_path}")
    except FileNotFoundError:
        print(f"训练数据未找到：{train_path}")
        return

    # 加载清洗后的测试数据
    test_path = os.path.join(
        project_root, "test_data", "processed",
        f"cleaned_test_building_{building}_floor_{floor}.csv"
    )
    try:
        test_df = pd.read_csv(test_path)
        print(f"成功加载测试数据：{test_path}")
    except FileNotFoundError:
        print(f"测试数据未找到：{test_path}")
        test_df = pd.DataFrame()

    # ====================== 2. 统一特征列并补全缺失列 ========================
    # 提取WAP特征列（以训练数据为基准）
    wap_columns = [col for col in train_df.columns if col.startswith('WAP')]
    
    # 处理测试数据
    if not test_df.empty:
        # 创建全量列模板（默认值-100）
        full_wap_df = pd.DataFrame(
            columns=wap_columns,
            data=np.full((len(test_df), len(wap_columns)), -100),
            dtype=np.float32
        )
        
        # 更新存在的列
        existing_cols = list(set(wap_columns) & set(test_df.columns))
        full_wap_df[existing_cols] = test_df[existing_cols].values
        
        # 合并其他元数据列
        test_df = pd.concat([
            full_wap_df,
            test_df[['BUILDINGID', 'FLOOR', 'LONGITUDE', 'LATITUDE']].reset_index(drop=True)
        ], axis=1)
    else:
        print(f"楼栋{building}楼层{floor}无测试数据")
        # 创建空DataFrame并填充默认值
        test_df = pd.DataFrame(columns=wap_columns + ['BUILDINGID', 'FLOOR', 'LONGITUDE', 'LATITUDE'])
        test_df[wap_columns] = -100

    # ====================== 3. 替换所有100为-100 ========================
    train_df[wap_columns] = train_df[wap_columns].replace(100, -100)
    test_df[wap_columns] = test_df[wap_columns].replace(100, -100)

    # ========================== 4. 合并数据集 ============================
    merged_df = pd.concat([train_df, test_df], axis=0, ignore_index=True)
    
    # ========================== 5. 保存数据 ============================
    merged_dir = os.path.join(project_root, "merged_data")
    os.makedirs(merged_dir, exist_ok=True)
    
    # 保存CSV
    csv_path = os.path.join(merged_dir, f"merged_building_{building}_floor_{floor}.csv")
    merged_df.to_csv(csv_path, index=False)
    print(f"合并数据已保存至：{csv_path}")
    
    # 保存MATLAB格式
    mat_path = os.path.join(merged_dir, f"merged_building_{building}_floor_{floor}.mat")
    scipy.io.savemat(mat_path, {
        'RSS': merged_df[wap_columns].astype(np.float32).values,
        'LOC': merged_df[['LONGITUDE', 'LATITUDE']].astype(np.float32).values
    })
    print(f"MATLAB数据已保存至：{mat_path}")

def main():
    """主函数：处理所有楼栋楼层组合"""
    # 配置需要处理的楼栋楼层组合
    building_floors = {
        0: [0, 1, 2, 3],
        1: [0, 1, 2, 3],
        2: [0, 1, 2, 3]
    }
    
    for building, floors in building_floors.items():
        for floor in floors:
            process_and_merge_data(building, floor)

if __name__ == "__main__":
    main()