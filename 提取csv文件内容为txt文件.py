import os
import pandas as pd

# ===== 配置路径 =====
csv_path = r"C:\Users\yichenlv\Desktop\UAV数据集\archive (2)\Test.csv"   # CSV 文件路径
output_dir = r"C:\Users\yichenlv\Desktop\UAV数据集\archive (2)\lable\val"   # 输出 txt 的文件夹

os.makedirs(output_dir, exist_ok=True)

# ===== 读取 CSV =====
df = pd.read_csv(csv_path)

required_cols = ["ID", "Confidence", "ymin", "xmin", "ymax", "xmax"]
for col in required_cols:
    if col not in df.columns:
        raise ValueError(f"CSV 中缺少列: {col}")

# ===== 按 ID 分组并导出 =====
for img_id, group in df.groupby("ID"):
    txt_path = os.path.join(output_dir, f"{img_id}.txt")

    with open(txt_path, "w", encoding="utf-8") as f:
        for _, row in group.iterrows():
            # line = f"{row['Confidence']} {row['ymin']} {row['xmin']} {row['ymax']} {row['xmax']}"
            line = f"0 {row['ymin']} {row['xmin']} {row['ymax']} {row['xmax']}"
            f.write(line + "\n")

    print(f"Saved: {txt_path}")

print("\nAll files generated successfully.")
