import os
import glob


def rename_paired_files(image_dir, label_dir):
    """
    将图片目录和标签目录下的成对文件（同名不同后缀）从1开始顺序重命名

    Args:
        image_dir (str): 图片文件目录路径
        label_dir (str): 标签文件目录路径
    """
    # 验证目录是否存在
    if not os.path.exists(image_dir):
        print(f"错误：图片目录不存在 -> {image_dir}")
        return
    if not os.path.exists(label_dir):
        print(f"错误：标签目录不存在 -> {label_dir}")
        return

    # 获取图片目录下的所有jpg文件（按文件名排序）
    image_files = sorted(glob.glob(os.path.join(image_dir, "*.jpg")))

    if not image_files:
        print("警告：图片目录下没有找到jpg文件")
        return

    # 遍历所有图片文件，进行成对重命名
    for idx, img_path in enumerate(image_files, start=1):
        # 获取原文件名（不含路径和后缀）
        img_filename = os.path.basename(img_path)
        file_name_without_ext = os.path.splitext(img_filename)[0]

        # 构建对应的标签文件路径
        label_path = os.path.join(label_dir, f"{file_name_without_ext}.txt")

        # 检查标签文件是否存在
        if not os.path.exists(label_path):
            print(f"警告：跳过不存在配对标签的图片 -> {img_filename}")
            continue

        # 构建新的文件路径
        new_img_name = f"{idx}.jpg"
        new_label_name = f"{idx}.txt"

        new_img_path = os.path.join(image_dir, new_img_name)
        new_label_path = os.path.join(label_dir, new_label_name)

        # 检查新文件名是否已存在（避免覆盖）
        if os.path.exists(new_img_path) or os.path.exists(new_label_path):
            print(f"错误：新文件名已存在，跳过 -> {new_img_name}/{new_label_name}")
            continue

        # 执行重命名
        os.rename(img_path, new_img_path)
        os.rename(label_path, new_label_path)

        print(f"成功重命名：")
        print(f"  图片：{img_filename} -> {new_img_name}")
        print(f"  标签：{file_name_without_ext}.txt -> {new_label_name}")
        print("-" * 40)


# 主程序
if __name__ == "__main__":
    # 定义文件路径（根据你的需求修改）
    IMAGE_DIR = r"F:\牛数据集\shuffled\images"
    LABEL_DIR = r"F:\牛数据集\shuffled\labels"

    # 执行重命名操作
    print("开始执行成对文件重命名...")
    print(f"图片目录：{IMAGE_DIR}")
    print(f"标签目录：{LABEL_DIR}")
    print("-" * 40)

    rename_paired_files(IMAGE_DIR, LABEL_DIR)

    print("重命名操作完成！")
