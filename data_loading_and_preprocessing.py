import os
from datasets import load_dataset
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
#load de-en dataset
de_en_dataset = load_dataset('json', data_files = 'WMT_deen.json')
#check the structure of dataset
#print(de_en_dataset.head(10))
en_zh_dataset = load_dataset('json', data_files = 'WMT_enzh.json')
#print(en_zh_dataset.head(10))

#split the data into training set\ validation set and test set
de_en_dataset = de_en_dataset["train"].train_test_split(test_size = 0.2)
de_en_dataset_split = de_en_dataset['test'].train_test_split(test_size=0.5)
de_en_dataset["test"] = de_en_dataset_split["test"]
de_en_dataset["validation"] = de_en_dataset_split["train"]

en_zh_dataset = en_zh_dataset["train"].train_test_split(test_size = 0.2)
en_zh_dataset_split = en_zh_dataset['test'].train_test_split(test_size=0.5)
en_zh_dataset["test"] = en_zh_dataset_split["test"]
en_zh_dataset["validation"] = en_zh_dataset_split["train"]

#check the lenth of datasets after splitting
#if __name__ == "__main__":
print("De-En Training Set:", len(de_en_dataset["train"]))
print("De-En Validation Set:", len(de_en_dataset["validation"]))
print("De-En Test Set:", len(de_en_dataset["test"]))
print("En-Zh Training Set:", len(en_zh_dataset["train"]))
print("En-Zh Validation Set:", len(en_zh_dataset["validation"]))
print("En-Zh Test Set:", len(en_zh_dataset["test"]))

os.environ["HTTP_PROXY"] = "http://127.0.0.1:7897"
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7897"
#load MBart model and tokenizer
model_name = 'facebook/mbart-large-50-many-to-many-mmt'
tokenizer = MBart50TokenizerFast.from_pretrained(model_name)

#tokenize the de-en dataset
def preprocess_function_deen(sentence_pairs):
    inputs = tokenizer(sentence_pairs['de'], padding = "max_length", truncation = True)
    targets = tokenizer(sentence_pairs['en'], padding = "max_length", truncation = True)
    inputs['labels'] = targets['input_ids']
    return inputs
de_en_dataset = de_en_dataset.map(preprocess_function_deen, batched = True)

#tokenize the en_zh dataset
def preprocess_function_enzh(sentence_pairs):
    inputs = tokenizer(sentence_pairs['en'], padding = 'max_length', truncation = True)
    targets = tokenizer(sentence_pairs['zh'], padding = 'max_length', truncation = True)
    inputs['labels'] = targets['input_ids']
    return inputs
en_zh_dataset = en_zh_dataset.map(preprocess_function_enzh, batched = True)
#check the datasets after processing
print(de_en_dataset['train'][0])
print(en_zh_dataset['train'][0])

