# ApertureStatsTool# ApertureStatsTool# RAW文件光圈统计工具

## 项目用途
本脚本用于统计分析指定目录下所有RAW格式照片的光圈使用频率，自动生成饼状图可视化结果并导出Excel格式的统计数据报表。

## 运行环境要求
- Python 3.8+
- 安装依赖库：`pip install matplotlib pandas tqdm`
- ExifTool工具：需下载[exiftool.exe](https://exiftool.org/)并置于系统PATH路径或脚本同级目录

## 配置说明
1. 修改脚本中的`image_directory`变量值为您的RAW文件存储路径
2. 确保exiftool.exe可执行文件位于以下位置之一：
   - 系统环境变量PATH包含的目录
   - 与脚本同级的工具目录

## 使用步骤
```bash
python tj.py
```

## 输出结果
1. 屏幕显示光圈使用百分比（保留两位小数）
2. 自动弹出饼状图窗口展示可视化结果
3. 生成Excel文件`aperture_percentages.xlsx`包含详细数据

## 支持格式
支持主流RAW格式：NEF、CR2、CR3、ARW、DNG等20+种相机原始格式

## 注意事项
1. 首次运行前请确保安装全部Python依赖
2. RAW文件路径不要包含中文或特殊字符
3. 处理大量文件时建议预留足够内存（每1000文件约需200MB）
4. Excel文件生成在脚本执行目录，多次运行会覆盖之前结果