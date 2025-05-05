#pzOq2QTSoggacdMOOC3n
import json
import requests
import hashlib
import random
import time

# 你的百度翻译 API 凭证
APP_ID = "20250327002316713"
SECRET_KEY = "pzOq2QTSoggacdMOOC3n"

def translate_batch_baidu(query, from_lang='en', to_lang='de'):
    """
    translate English data to German
    """
    url = "http://api.fanyi.baidu.com/api/trans/vip/translate"
    salt = str(random.randint(32768, 65536))
    sign_str = APP_ID + query + salt + SECRET_KEY
    sign = hashlib.md5(sign_str.encode()).hexdigest()

    params = {
        "q": query,
        "from": from_lang,
        "to": to_lang,
        "appid": APP_ID,
        "salt": salt,
        "sign": sign
    }

    try:
        response = requests.get(url, params=params)
        result = response.json()
        if "trans_result" in result:
            return result["trans_result"][0]["dst"]
        else:
            print(f"translation failed:{result}")
            return None
    except Exception as e:
        print(f"request failed:{e}")
        return None

# set paths of input data
input_file = "C:/Users/DELL/Desktop/folderforall/本科毕业论文/DL_news_translation/data_expansion/compare_baidu_deepL/compare_enzh.json"
output_file = "baidu_compare_translated_entode.json"

# load json file
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

print('finished loading, translation begins...')


for i, item in enumerate(data):
    en_text = item.get("en", "")
    if en_text:
        translated = translate_batch_baidu(en_text, from_lang="en", to_lang="de")
        print(f"[{i+1}] original text: {en_text} | translation: {translated}")
        item["de"] = translated

print("translation finished")

# write in new json file
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"output file saved to:{output_file}")