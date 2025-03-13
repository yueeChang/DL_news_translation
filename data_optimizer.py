from transformers import BertTokenizer, BertForMaskedLM, T5Tokenizer, T5ForConditionalGeneration
import torch

# Initialize BERT for grammar correction
bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
bert_model = BertForMaskedLM.from_pretrained('bert-base-uncased')

# Initialize T5 for fluency improvement
t5_tokenizer = T5Tokenizer.from_pretrained('t5-small')
t5_model = T5ForConditionalGeneration.from_pretrained('t5-small')

def correct_grammar_with_bert(text):
    # Tokenize the input text
    inputs = bert_tokenizer(text, return_tensors="pt")
    
    # Predict masked words (BERT works by filling in missing words to improve syntax)
    with torch.no_grad():
        predictions = bert_model(**inputs).logits

    # Get the predicted token ids and decode them back to words
    predicted_ids = torch.argmax(predictions, dim=-1)
    corrected_text = bert_tokenizer.decode(predicted_ids[0], skip_special_tokens=True)
    
    return corrected_text

def improve_fluency_with_t5(text):
    # Prepare the text for T5 (T5 requires a task-specific prefix)
    input_text = "translate English to German: " + text  # This assumes we are optimizing English to German translation
    inputs = t5_tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)

    # Generate a more fluent translation
    with torch.no_grad():
        outputs = t5_model.generate(input_ids=inputs.input_ids, max_length=512)
    
    # Decode the generated text
    fluent_text = t5_tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return fluent_text

def optimize_translations(de_zh_data):
    optimized_data = []
    
    for entry in de_zh_data:
        original_translation = entry["zh"]  # Assuming the Chinese translations are under 'zh'
        
        # Step 1: Use BERT for grammar correction
        corrected_translation = correct_grammar_with_bert(original_translation)
        
        # Step 2: Use T5 to improve the fluency of the text
        fluent_translation = improve_fluency_with_t5(corrected_translation)
        
        # Store the optimized translation
        optimized_data.append({
            "original": original_translation,
            "corrected": corrected_translation,
            "fluent": fluent_translation
        })
    
    return optimized_data