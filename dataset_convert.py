import os
import cv2
import json
from tqdm import tqdm
import argparse

name = 'val' # train, val, test
dataset_name = 'data/CMBD'

parser = argparse.ArgumentParser()
parser.add_argument('--root_dir', default=dataset_name, type=str, help="root path of images and labels, include ./images and ./labels and classes.txt")
parser.add_argument('--save_path', type=str, default=f'instances_{name}.json', help="if not split the dataset, give a path to a json file")

arg = parser.parse_args()

def yolo2coco(arg):
    root_path = arg.root_dir
    print("Loading data from ", root_path)

    assert os.path.exists(root_path), f"root path not found: {root_path}"
    originLabelsDir = os.path.join(root_path, f'labels/{name}')
    originImagesDir = os.path.join(root_path, f'images/{name}')

    if not os.path.isdir(originImagesDir):
        raise FileNotFoundError(f"Images dir not found: {originImagesDir}")
    if not os.path.isdir(originLabelsDir):
        print(f"Warning: labels dir not found: {originLabelsDir} (will skip missing labels)")

    classes_file = os.path.join(root_path, 'classes.txt')
    if not os.path.exists(classes_file):
        raise FileNotFoundError(f"classes.txt not found in {root_path}")
    with open(classes_file) as f:
        classes = list(map(lambda x: x.strip(), f.readlines()))

    indexes = sorted(os.listdir(originImagesDir))

    dataset = {'categories': [], 'annotations': [], 'images': []}
    for i, cls in enumerate(classes, 0):
        dataset['categories'].append({'id': i, 'name': cls, 'supercategory': 'mark'})

    ann_id_cnt = 0
    failed_files = []

    for k, index in enumerate(tqdm(indexes, desc="Processing images")):
        try:
            # 构建 txt 文件名（与图片名对应）
            txtFile = index.replace('images','txt').replace('.jpg','.txt').replace('.png','.txt')

            img_path = os.path.join(originImagesDir, index)
            im = cv2.imread(img_path)
            if im is None:
                raise RuntimeError(f"Failed to read image or image is corrupted: {img_path}")
            height, width, _ = im.shape

            label_path = os.path.join(originLabelsDir, txtFile)
            # 若标签不存在，则仍保留图片信息但跳过 annotation 部分
            dataset['images'].append({
                'file_name': index,
                'id': int(index[:-4]) if index[:-4].isnumeric() else index[:-4],
                'width': width,
                'height': height
            })

            if not os.path.exists(label_path):
                # 没有标签文件，跳过 annotations
                continue

            with open(label_path, 'r') as fr:
                labelList = fr.readlines()

            for line_no, label in enumerate(labelList, start=1):
                try:
                    parts = label.strip().split()
                    if len(parts) < 5:
                        # 非法行，跳过并打印提示
                        print(f"  ⚠️  skip invalid label line: {label_path} (line {line_no})")
                        continue

                    cls_id = int(parts[0])
                    x = float(parts[1])
                    y = float(parts[2])
                    w = float(parts[3])
                    h = float(parts[4])

                    H, W, _ = im.shape
                    x1 = (x - w / 2) * W
                    y1 = (y - h / 2) * H
                    x2 = (x + w / 2) * W
                    y2 = (y + h / 2) * H

                    bbox_w = max(0.0, x2 - x1)
                    bbox_h = max(0.0, y2 - y1)

                    dataset['annotations'].append({
                        'area': bbox_w * bbox_h,
                        'bbox': [x1, y1, bbox_w, bbox_h],
                        'category_id': cls_id,
                        'id': ann_id_cnt,
                        'image_id': int(index[:-4]) if index[:-4].isnumeric() else index[:-4],
                        'iscrowd': 0,
                        'segmentation': [[x1, y1, x2, y1, x2, y2, x1, y2]]
                    })
                    ann_id_cnt += 1
                except Exception as e_line:
                    # 单行解析失败，记录并继续处理该文件的其它行
                    print(f"  ❌ Error parsing line {line_no} in {label_path}: {e_line}")
                    continue

        except Exception as e:
            # 整个文件处理失败，记录文件名并继续
            failed_files.append(index)
            print(f"❗ Failed to process file {index}: {e}")

    # 保存结果
    os.makedirs(os.path.dirname(arg.save_path) or '.', exist_ok=True)
    try:
        with open(arg.save_path, 'w') as f:
            json.dump(dataset, f)
            print('Save annotation to {}'.format(arg.save_path))
    except Exception as e:
        print(f"❌ Failed to save json to {arg.save_path}: {e}")

    # 汇总失败文件
    if failed_files:
        print("\n===== Summary: Failed files =====")
        for fn in failed_files:
            print(fn)
        print(f"Total failed: {len(failed_files)}")
    else:
        print("\nAll files processed successfully.")

if __name__ == "__main__":
    yolo2coco(arg)