import os
from transformers import MBart50TokenizerFast, MBartForConditionalGeneration

# Load pre-trained mBART model and tokenizer for German -> Chinese translation
os.environ["HTTP_PROXY"] = "http://127.0.0.1:7897"
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7897"
#load MBart model and tokenizer
model_name = 'facebook/mbart-large-50-many-to-many-mmt'
tokenizer = MBart50TokenizerFast.from_pretrained(model_name)
model = MBartForConditionalGeneration.from_pretrained(model_name)

src_lang = "de_DE"  # German
tgt_lang = "zh_CN"  # Chinese

# Example German sentence to be translated to Chinese
de_sentence = "Für die kommenden 3-4 Monate gehen Analysten von einer 3-Prozent-Inflationsrate aus, beziffern die jährliche Durchschnittsrate aber mit 2,1 Prozent."

# Tokenize the input sentence (German)
inputs = tokenizer(de_sentence, return_tensors="pt", padding=True, truncation=True)

# Force the model to generate a translation in the target language (Chinese)
# Use the bos_token for the target language
forced_bos_token_id = tokenizer.lang_code_to_id[tgt_lang]

# Perform translation (generate method to get translated tokens)
translated = model.generate(**inputs, forced_bos_token_id=forced_bos_token_id)

# Decode the translated tokens back to Chinese text
translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)

# Print the original and translated sentences
print(f"Original German: {de_sentence}")
print(f"Translated Chinese: {translated_text}")