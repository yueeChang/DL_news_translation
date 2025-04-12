import json
import requests

def translate_deeplx(text, source_lang="EN", target_lang="ZH"):
    #translate with DeepLX
    url = "https://api.deeplx.org/v2/translate"
    payload = {
        "text": text,
        "source_lang": source_lang.upper(),
        "target_lang": target_lang.upper()
    }
    response = requests.post(url, json=payload)
    return response.json().get("translations", [{}])[0].get("text", "")

#read the de-en data
input_file = "WMT_deen.json"
output_file = "WMT_deenzh.json"

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)  # 读取 JSON 数据

# 2. 遍历 JSON 数据并翻译 en 部分
for item in data:
    en_text = item.get("en", "")  # 获取英语文本
    if en_text:
        translated_text = translate_deeplx(en_text, "EN", "ZH")  # 翻译到中文
        item["zh"] = translated_text  # 添加翻译后的文本

# 3. 保存回 JSON 文件
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)  # 确保中文正常保存

print(f"翻译完成，结果已保存到 {output_file}")