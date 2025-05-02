import json
import requests
import time

DEEPL_API_KEY = "c9e296d4-0689-4c25-8451-bf953d0af898"
DEEPL_URL = "https://api.deepl.com/v2/translate"
def translate_deepl(text, source_lang="EN", target_lang="DE"):
    params = {
        "auth_key": DEEPL_API_KEY,
        "text": text,
        "source_lang": source_lang,
        "target_lang": target_lang
    }
    try:
    
        response = requests.post(DEEPL_URL, data=params, proxies={"http": None, "https": None})
        #print(f"Response: {response.text}")
        response.raise_for_status()
        result = response.json()
        #print(result)
        translations = result.get("translations")
        if translations and isinstance(translations, list):
            return translations[0].get("text")
        return None
    except requests.exceptions.RequestException as e:
        print(f"request error: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
        return None

#print(translate_deepl("Hello, world!", "EN", "DE"))
#read the de-en data
input_file = "C:/Users/DELL/Desktop/folderforall/本科毕业论文/DL_news_translation/data_expansion/WMT_enzh_trial.json"
output_file = "deepL_entode.json"
#print('准备就绪 ready to translate')
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)  # 读取 JSON 数据
print('finishing loading the data')
# 2. 遍历 JSON 数据并翻译 en 部分
for i, item in enumerate(data):
    en_text = item.get("en", "")  # 获取英语文本
    if en_text:
        translated_text = translate_deepl(en_text, "EN", "DE")  # 翻译到中文
        print(i+1)
        item["DE"] = translated_text  # 添加翻译后的文本
       # time.sleep(0.2)
print('finished translation')
# 3. 保存回 JSON 文件a
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)  # 确保中文正常保存

print(f"Output file saved to {output_file}")