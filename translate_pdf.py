import os
import fitz  # pymupdf
from markdownify import markdownify as md

# 1. 配置路径（确保路径正确）
INPUT_DIR = "input_pdf"
OUTPUT_DIR = "output"

# 2. 创建output文件夹（确保存在）
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 3. 获取input_pdf里的所有PDF文件
pdf_files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".pdf")]

if not pdf_files:
    print("⚠️ 未找到input_pdf文件夹中的PDF文件")
else:
    for pdf_file in pdf_files:
        # 拼接完整路径
        pdf_path = os.path.join(INPUT_DIR, pdf_file)
        # 提取文件名（不带后缀）
        file_name = os.path.splitext(pdf_file)[0]
        
        try:
            # 步骤1：读取PDF内容（仅解析文本，暂不翻译）
            doc = fitz.open(pdf_path)
            raw_text = ""
            for page in doc:
                raw_text += page.get_text()
            doc.close()
            
            # 步骤2：生成纯文本文件（暂不翻译，先验证流程）
            txt_path = os.path.join(OUTPUT_DIR, f"{file_name}_原始文本.txt")
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(raw_text)
            
            # 步骤3：生成MD文件（原始文本转MD）
            md_path = os.path.join(OUTPUT_DIR, f"{file_name}_原始文本.md")
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(md(raw_text))
            
            # 步骤4：生成空的双语PDF标记文件（后续补翻译）
            pdf_marker = os.path.join(OUTPUT_DIR, f"{file_name}_双语PDF_待翻译.txt")
            with open(pdf_marker, "w", encoding="utf-8") as f:
                f.write("PDF翻译功能待补充：需配置siliconflow API后启用\n")
            
            print(f"✅ 成功处理 {pdf_file}，生成原始文本文件到output文件夹")
        
        except Exception as e:
            print(f"❌ 处理 {pdf_file} 失败：{str(e)}")

print("🎉 基础流程执行完成（暂未翻译，仅解析PDF文本）")