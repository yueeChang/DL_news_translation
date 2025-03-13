import json
import requests
import random
import data_optimizer as do
from sklearn.model_selection import train_test_split

# Step 1: Load the data
def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Step 2: Translate text using DeepL API
def translate_text(text, target_lang, api_key):
    url = "https://api-free.deepl.com/v2/translate"
    params = {
        "auth_key": api_key,
        "text": text,
        "target_lang": target_lang,
    }
    response = requests.post(url, data=params)
    result = response.json()
    return result["translations"][0]["text"]

# Step 3: Translate the datasets
def translate_data(de_en_data, en_zh_data, api_key):
    de_zh_data = []
    
    # Translate de-en to de-zh
    for entry in de_en_data:
        en_text = entry["en"]
        zh_translation = translate_text(en_text, "ZH", api_key)
        de_zh_data.append({"de": entry["de"], "zh": zh_translation})

    # Translate en-zh to de-zh
    for entry in en_zh_data:
        en_text = entry["en"]
        de_translation = translate_text(en_text, "DE", api_key)
        de_zh_data.append({"de": de_translation, "zh": entry["zh"]})

    return de_zh_data


# Step 5: Merge and split the data into training and testing sets
def split_data(de_zh_data):
    train_data, test_data = train_test_split(de_zh_data, test_size=0.2, random_state=42)
    return train_data, test_data

# Main function to run the entire process
def main():
    # Load the datasets
    de_en_data = load_data('C:\Users\DELL\Desktop\folderforall\本科毕业论文\DL_news_translation\WMT_deen.json')  # Replace with your actual file paths
    en_zh_data = load_data('C:\Users\DELL\Desktop\folderforall\本科毕业论文\DL_news_translation\WMT_enzh.json')  # Replace with your actual file paths

    # Your DeepL API key
    api_key = '3dc7a246-20dc-427f-9961-6634c7138b53:fx'  # Replace with your DeepL API Key

    # Step 2: Translate the data
    de_zh_data = translate_data(de_en_data, en_zh_data, api_key)

    # Step 3: Optimize the translations
    optimized_data = do.optimize_translations(de_zh_data)

    # Step 4: Split the data into training and testing sets
    train_data, test_data = split_data(optimized_data)

    # Save the datasets
    with open('train_data.json', 'w', encoding='utf-8') as f:
        json.dump(train_data, f, ensure_ascii=False, indent=4)
    
    with open('test_data.json', 'w', encoding='utf-8') as f:
        json.dump(test_data, f, ensure_ascii=False, indent=4)

    print("Data processing complete. Training and testing sets saved.")

if __name__ == "__main__":
    main()