'''
将文件从1重新编号。
'''

import os

# 修改为你的文件夹路径
folder_path = r"C:\Users\yichenlv\Desktop\output"

# 获取文件列表（只保留文件）
files = [
    f for f in os.listdir(folder_path)
    if os.path.isfile(os.path.join(folder_path, f))
]

# 按文件名排序（很重要）
files.sort()

# 重新编号
for index, filename in enumerate(files, start=1):
    old_path = os.path.join(folder_path, filename)

    # 拆分文件名和后缀
    _, ext = os.path.splitext(filename)

    # 新文件名
    new_name = f"{index}{ext}"
    new_path = os.path.join(folder_path, new_name)

    os.rename(old_path, new_path)

print("文件重命名完成！")
