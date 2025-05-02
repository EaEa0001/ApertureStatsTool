import os
import subprocess
import json
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import pandas as pd

# 每个批次处理的文件数量
BATCH_SIZE = 50

def get_common_raw_extensions():
    return {'.nef', '.cr2', '.cr3', '.arw', '.dng', '.orf', '.pef', '.sr2', '.srw', '.rw2', '.nrw', '.x3f'}

def is_raw_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    return ext in get_common_raw_extensions()

def parse_raw_exif_batch(file_paths):
    try:
        command = ['exiftool.exe', '-j'] + file_paths
        result = subprocess.run(command, capture_output=True)
        # 指定使用 utf-8 编码解码输出
        output = result.stdout.decode('utf-8', errors='replace')
        if output:
            exif_data = json.loads(output)
            apertures = []
            for data in exif_data:
                aperture = data.get('FNumber')
                apertures.append(aperture)
            return apertures
        else:
            print(f"读取 RAW 文件批次 {file_paths} 时输出为空")
    except json.JSONDecodeError as e:
        print(f"解析 JSON 数据失败: {str(e)}，输出内容: {output[:200]}")
    except Exception as e:
        print(f"读取 RAW 文件批次失败: {str(e)}")
    return [None] * len(file_paths)

def process_file_batch(file_paths):
    return parse_raw_exif_batch(file_paths)

image_directory = 'H:\\拍的还行\\2025_3_28虹口足球场'
raw_files = []

# 收集所有 RAW 文件
for root, dirs, files in os.walk(image_directory):
    for file in files:
        file_path = os.path.join(root, file)
        if is_raw_file(file_path):
            raw_files.append(file_path)

aperture_counts = {}
total_raw_files = len(raw_files)

# 按批次划分文件
file_batches = [raw_files[i:i + BATCH_SIZE] for i in range(0, total_raw_files, BATCH_SIZE)]

# 使用线程池并行处理文件批次
with ThreadPoolExecutor() as executor:
    all_apertures = []
    results = list(tqdm(executor.map(process_file_batch, file_batches), total=len(file_batches), desc="处理文件批次进度"))
    for batch_apertures in results:
        all_apertures.extend(batch_apertures)

# 统计光圈出现次数
for aperture in all_apertures:
    if aperture is not None:
        aperture_str = f"f/{aperture:.2f}"
        if aperture_str in aperture_counts:
            aperture_counts[aperture_str] += 1
        else:
            aperture_counts[aperture_str] = 1

# 计算各光圈的百分比
aperture_percentages = {}
for aperture, count in aperture_counts.items():
    aperture_percentages[aperture] = (count / total_raw_files) * 100

# 打印各光圈的百分比
for aperture, percentage in aperture_percentages.items():
    print(f"{aperture}: {percentage:.2f}%")

# 生成饼图
labels = list(aperture_percentages.keys())
sizes = list(aperture_percentages.values())
plt.pie(sizes, labels=labels, autopct='%1.2f%%')
plt.axis('equal')
plt.title('各光圈出现的百分比')
plt.show()

# 输出到 Excel
try:
    df = pd.DataFrame.from_dict(aperture_percentages, orient='index', columns=['百分比(%)'])
    df.index.name = '光圈'
    df.to_excel('aperture_percentages.xlsx')
    print("数据已成功输出到 aperture_percentages.xlsx 文件。")
except Exception as e:
    print(f"输出到 Excel 文件时出现错误: {e}")
    