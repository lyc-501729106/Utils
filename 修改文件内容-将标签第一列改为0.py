import os

txt_dir = r"C:\Users\yichenlv\Desktop\UAV数据集\archive (1)\WAID-final - Copy\labels\test"  # 存放 .txt 文件的文件夹

for filename in os.listdir(txt_dir):
    if not filename.lower().endswith(".txt"):
        continue

    file_path = os.path.join(txt_dir, filename)

    new_lines = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split()
            if len(parts) != 5:
                # 行格式不符合时，原样保留（安全）
                new_lines.append(line)
                continue

            parts[0] = "0"
            new_lines.append(" ".join(parts))

    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines) + "\n")

    print(f"Processed: {filename}")

print("\nAll txt files processed.")
