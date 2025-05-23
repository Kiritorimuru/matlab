# src/merge_data.py
import os
import pandas as pd
import numpy as np
import scipy.io

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def merge_and_save(building, floor, use_wgan=True):
    # 加载清洗后的真实数据
    cleaned_path = os.path.join(
        project_root, "data", "processed",
        f"cleaned_building_{building}_floor_{floor}.csv"
    )
    real_data = pd.read_csv(cleaned_path)
    
    # 加载生成数据
    gen_file_name = f"synthetic_data_{'wgan' if use_wgan else 'cgan'}_building_{building}_floor_{floor}.csv"
    gen_path = os.path.join(project_root, "generated_samples", gen_file_name)
    gen_data = pd.read_csv(gen_path)
    
    # 合并数据
    merged_data = pd.concat([real_data, gen_data], axis=0)
    
    # 提取RSS和LOC
    wap_columns = [col for col in real_data.columns if col.startswith('WAP')]
    RSS = merged_data[wap_columns].values
    LOC = merged_data[['LONGITUDE', 'LATITUDE']].values
    
    # 保存为.mat文件
    save_dir = os.path.join(project_root, "matlab_data")
    os.makedirs(save_dir, exist_ok=True)
    scipy.io.savemat(
        os.path.join(save_dir, f"merged_building_{building}_floor_{floor}.mat"),
        {'RSS': RSS, 'LOC': LOC}
    )
    print(f"合并数据已保存至: {save_dir}/merged_building_{building}_floor_{floor}.mat")

if __name__ == "__main__":
    merge_and_save(building=0, floor=3, use_wgan=True)