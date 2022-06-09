from scrapy import cmdline
# 导入cmdline模块,可以实现控制终端命令行。
import os    # 用来设置路径
import sys   # 调用系统环境，就如同cmd中执行命令一样

# 获取当前脚本路径
dirpath = os.path.dirname(os.path.abspath(__file__))
# 运行文件绝对路径
# print(os.path.abspath(__file__))
# 运行文件父路径

# print(dirpath)
# 添加环境变量
sys.path.append(dirpath)
# 切换工作目录
os.chdir(dirpath)

cmdline.execute(['scrapy','crawl','simple'])
# 用execute（）方法，输入运行scrapy的命令。

# import csv
# f = open(r"D:\python\reptile\4.数据定位\uooc\Uooc\1.csv", "a", newline="", encoding="utf-8")
# # 设置文件第一行的字段名，注意要跟spider传过来的字典key名称相同
# fieldnames = [
#     "chapter_name",
#     "sub_name",
#     "sub_url",
#     "caption",
#     "choice",
#     ]
# writer = csv.DictWriter(f, fieldnames=fieldnames)
# # 写入第一行字段名，因为只要写入一次，所以文件放在__init__里面
# writer.writeheader()
# writer.writerow({
#     "chapter_name":"-----------",
#     "sub_name":"-----------",
#     "sub_url":"-----------",
#     "caption":"-----------",
#     "choice":"-----------",
# })

# import pandas as pd
# url_df = pd.read_excel(r"D:\python\reptile\4.数据定位\uooc\chapter.xlsx",sheet_name="Sheet1")
# url_df = url_df.iloc[2:,:]
# print(url_df)
# print([url_df["url"][2]])
# print(url_df["name"][2])