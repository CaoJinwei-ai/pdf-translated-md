import os
import sys
import fitz  # PyMuPDF，处理PDF
import pdf2zh
from markdownify import markdownify  # PDF转MD
from siliconflow import ChatClient  # 硅基流动SDK

# 1. 配置参数
INPUT_DIR = "./input_pdf"  # 输入PDF文件夹
OUTPUT_DIR = "./output"    # 输出文件夹
API_KEY = os.getenv("SILICONFLOW_API_KEY")  # 从GitHub Secrets获取API Key

# 2. 创建输出文件夹
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 3. 初始化翻译客户端（DeepSeek V3）
client = ChatClient(api_key=API_KEY)
def translate_text(text):
    """调用DeepSeek V3翻译文本（英文→中文）"""
    response = client.chat.completions.create(
        model="deepseek-chat",  # DeepSeek V3模型名
        messages=[
            {"role": "system", "content": "你是专业的技术文档翻译助手，翻译英文技术文档到中文，保留专业术语准确性，语句通顺，不增不减语义。"},
            {"role": "user", "content": f"翻译以下文本：{text}"}
        ],
        temperature=0.1  # 翻译更精准，避免乱编
    )
    return response.choices[0].message.content

# 4. 处理PDF：解析→翻译→生成双语/纯中文PDF+转MD
def process_pdf(pdf_path):
    # 获取PDF文件名（不含后缀）
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    
    # 步骤1：用pdf2zh解析PDF并翻译（保留格式）
    # 生成双语PDF
    bilingual_pdf = f"{OUTPUT_DIR}/{pdf_name}_双语版.pdf"
    pdf2zh.translate_pdf(
        input_path=pdf_path,
        output_path=bilingual_pdf,
        translator=translate_text,  # 用DeepSeek翻译
        keep_original=True  # 保留原文，生成双语
    )
    
    # 生成纯中文PDF
    cn_pdf = f"{OUTPUT_DIR}/{pdf_name}_中文版.pdf"
    pdf2zh.translate_pdf(
        input_path=pdf_path,
        output_path=cn_pdf,
        translator=translate_text,
        keep_original=False  # 不保留原文，纯中文
    )
    
    # 步骤2：PDF转MD（以双语版为例）
    doc = fitz.open(bilingual_pdf)
    md_content = ""
    for page in doc:
        md_content += page.get_text() + "\n\n"
    md_content = markdownify(md_content)  # 转MD格式
    md_file = f"{OUTPUT_DIR}/{pdf_name}.md"
    with open(md_file, "w", encoding="utf-8") as f:
        f.write(md_content)
    
    print(f"✅ 处理完成：\n- 双语PDF：{bilingual_pdf}\n- 纯中文PDF：{cn_pdf}\n- MD文件：{md_file}")

# 5. 遍历input_pdf文件夹，处理所有PDF
if __name__ == "__main__":
    for file in os.listdir(INPUT_DIR):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(INPUT_DIR, file)
            print(f"🚀 开始处理PDF：{pdf_path}")
            process_pdf(pdf_path)