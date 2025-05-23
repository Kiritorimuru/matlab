# convert_test_data.py
import pandas as pd
import scipy.io
import os

# 项目根目录
project_root = os.path.dirname(os.path.abspath(__file__))

# 读取验证数据
val_data = pd.read_csv(os.path.join(project_root, "data", "UJIndoorLoc", "validationData.csv"))

# 提取指定楼层的测试数据（示例：楼0层3）
building, floor = 0, 3
val_data = val_data[(val_data['BUILDINGID'] == building) & (val_data['FLOOR'] == floor)]

# 提取WAP特征（需与实际列名匹配）
wap_columns = [f'WAP{i:03d}' for i in range(1, 521)]
testrss = val_data[wap_columns].values
testloc = val_data[['LONGITUDE', 'LATITUDE']].values

# 创建测试数据目录
test_data_dir = os.path.join(project_root, "test_data")
os.makedirs(test_data_dir, exist_ok=True)

# 保存为.mat文件
scipy.io.savemat(os.path.join(test_data_dir, "testrss.mat"), {'testrss': testrss})
scipy.io.savemat(os.path.join(test_data_dir, "testloc.mat"), {'testloc': testloc})

print(f"测试数据已保存至：{test_data_dir}")