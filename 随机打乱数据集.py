import os
import shutil
import random

def shuffle_pairs(
    image_dir,
    label_dir,
    out_image_dir,
    out_label_dir,
    image_ext=".jpg",
    label_ext=".txt"
):
    os.makedirs(out_image_dir, exist_ok=True)
    os.makedirs(out_label_dir, exist_ok=True)

    # 获取文件名（不含后缀）
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

    # 只保留成对存在的样本
    common_names = sorted(image_names & label_names)

    if not common_names:
        raise RuntimeError("❌ 没有找到任何成对的 jpg 和 txt")

    print(f"✅ Found {len(common_names)} paired samples")

    # 随机打乱
    random.shuffle(common_names)

    # 拷贝并重新编号
    for i, name in enumerate(common_names):
        new_name = f"{i:06d}"

        src_img = os.path.join(image_dir, name + image_ext)
        src_txt = os.path.join(label_dir, name + label_ext)

        dst_img = os.path.join(out_image_dir, new_name + image_ext)
        dst_txt = os.path.join(out_label_dir, new_name + label_ext)

        shutil.copy2(src_img, dst_img)
        shutil.copy2(src_txt, dst_txt)

    print("🎉 Shuffle completed successfully!")


if __name__ == "__main__":
    shuffle_pairs(
        image_dir=r"F:\牛数据集\UAV_CATTLE2\images\train",
        label_dir=r"F:\牛数据集\UAV_CATTLE2\labels\train",
        out_image_dir=r"F:\牛数据集/shuffled/images",
        out_label_dir=r"F:\牛数据集/shuffled/labels"
    )
