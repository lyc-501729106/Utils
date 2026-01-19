import os

'''
将.jpg文件与.txt文件没有匹配的打印出来 
'''
def check_image_txt_match(image_dir, label_dir, image_ext=".jpg", label_ext=".txt"):
    # 取文件名（不含后缀）
    image_names = {
        os.path.splitext(f)[0]
        for f in os.listdir(image_dir)
        if f.lower().endswith(image_ext)
    }

    label_names = {
        os.path.splitext(f)[0]
        for f in os.listdir(label_dir)
        if f.lower().endswith(label_ext)
    }

    # 差集
    images_without_labels = image_names - label_names
    labels_without_images = label_names - image_names

    # 输出结果
    if images_without_labels:
        print("❌ 图片存在但没有对应 txt：")
        for name in sorted(images_without_labels):
            print(f"  {name}{image_ext}")
    else:
        print("✅ 所有图片都有对应的 txt")

    print()

    if labels_without_images:
        print("❌ txt 存在但没有对应图片：")
        for name in sorted(labels_without_images):
            print(f"  {name}{label_ext}")
    else:
        print("✅ 所有 txt 都有对应的图片")


if __name__ == "__main__":
    image_dir = r"F:\牛数据集\UAV_CATTLE2\images\val"   # 修改为你的 images 目录
    label_dir = r"F:\牛数据集\UAV_CATTLE2\labels\val"   # 修改为你的 labels 目录

    check_image_txt_match(image_dir, label_dir)
