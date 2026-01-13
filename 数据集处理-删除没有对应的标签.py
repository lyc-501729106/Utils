'''
将没有对应的.txt文件删除掉
'''


import os

jpg_dir = r"C:\Users\yichenlv\Desktop\UAV数据集\archive (1)\WAID-final - Copy\images\test"   # 存放 .jpg 的文件夹
txt_dir = r"C:\Users\yichenlv\Desktop\UAV数据集\archive (1)\WAID-final - Copy\labels\test"   # 存放 .txt 的文件夹

# 获取 jpg 文件名（不含后缀）
jpg_names = {
    os.path.splitext(f)[0]
    for f in os.listdir(jpg_dir)
    if f.lower().endswith(".jpg")
}

deleted_count = 0

for txt_file in os.listdir(txt_dir):
    if not txt_file.lower().endswith(".txt"):
        continue

    txt_name = os.path.splitext(txt_file)[0]

    # 如果 txt 没有对应的 jpg
    if txt_name not in jpg_names:
        txt_path = os.path.join(txt_dir, txt_file)
        os.remove(txt_path)
        deleted_count += 1
        print(f"Deleted: {txt_file}")

print(f"\nDone. Deleted {deleted_count} txt files.")
