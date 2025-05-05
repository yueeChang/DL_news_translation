import json
import requests

DEEPL_API_KEY = "c9e296d4-0689-4c25-8451-bf953d0af898"
DEEPL_URL = "https://api.deepl.com/v2/translate"
BATCH_SIZE = 20  # translate 15 pieces of news at one time

def translate_batch_deepl(texts, source_lang="EN", target_lang="ZH"):
    """
    load a list of texts
    """
    params = {
        "auth_key": DEEPL_API_KEY,
        "source_lang": source_lang,
        "target_lang": target_lang,
    }
    # add parameters
    for t in texts:
        params.setdefault("text", []).append(t)

    try:
        response = requests.post(DEEPL_URL, data=params, proxies={"http": None, "https": None})
        response.raise_for_status()
        result = response.json()
        translations = result.get("translations", [])
        return [t.get("text") for t in translations]
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return [None] * len(texts)  # make sure the number of translation == number of input news
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return [None] * len(texts)

# file paths
input_file = "C:/Users/DELL/Desktop/folderforall/本科毕业论文/DL_news_translation/data_expansion/WMT_deen.json"
output_file = "deepL_entozh.json"

# load th edata
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)
print('Finished loading the data')

# collect index
text_list = []
index_list = []
for i, item in enumerate(data):
    if "en" in item and item["en"]:
        text_list.append(item["en"])
        index_list.append(i)

# begine with the translation
print('Translation begins...')
for i in range(0, len(text_list), BATCH_SIZE):
    batch_texts = text_list[i:i + BATCH_SIZE]
    batch_indices = index_list[i:i + BATCH_SIZE]
    translated_texts = translate_batch_deepl(batch_texts, "EN", "ZH")
    
    for j, translated in enumerate(translated_texts):
        data[batch_indices[j]]["ZH"] = translated
    print(f"Translating {i + len(batch_texts)} / {len(text_list)} ")

print('Translation finished...')
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"Output file saved to {output_file}")