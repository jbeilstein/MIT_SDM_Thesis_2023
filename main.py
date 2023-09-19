import requests
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text

bert_encoder_url = 'https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/4'
bert_encoder_model = hub.KerasLayer(bert_encoder_url)

bert_preprocessed_model_url = 'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3'
bert_preprocess_model = hub.KerasLayer(bert_preprocessed_model_url)

#text_sample = ['how now brown cow?','this is possibly the most amazing thing ever','do you understand this sentence?','i for one welcome our new AI overlords']
text_sample = ['this is a test, this is only a test']

####Pre-process sample text
text_preprocessed = bert_preprocess_model(text_sample)

sample_keys = text_preprocessed.keys()
sample_mask = text_preprocessed['input_mask']
sample_word_ids = text_preprocessed['input_word_ids']
sample_type_ids = text_preprocessed['input_type_ids']

print(sample_mask)
print(sample_word_ids)
print(sample_type_ids)
print(text_preprocessed)

####Encode pre-processed sample text
bert_encoded = bert_encoder_model(text_preprocessed)
bert_encoded_keys = bert_encoded.keys
bert_encoded_embeddings = bert_encoded['default']

print(bert_encoded_embeddings)

#model = hub.KerasLayer("https://tfhub.dev/google/nnlm-en-dim128/2")
#embeddings = model(["The rain in Spain.", "falls",
#                      "mainly", "In the plain!"])

####Tokenization goes here
tokenizer_white_space = text.WhitespaceTokenizer()
tokens_white_space = tokenizer_white_space.tokenize(["What you know you can't explain, but you feel it."])
print(tokens_white_space.to_list())

tokenizer_unicode = text.UnicodeScriptTokenizer()
tokens_unicode = tokenizer_unicode.tokenize(["What you know you can't explain, but you feel it."])
print(tokens_unicode.to_list())

url = "https://github.com/tensorflow/text/blob/master/tensorflow_text/python/ops/test_data/test_wp_en_vocab.txt?raw=true"
r = requests.get(url)
filepath = "vocab.txt"
open(filepath, 'wb').write(r.content)

tokenizer_unicode = text.UnicodeScriptTokenizer(filepath)
# subtokens_unicode = tokenizer_unicode.tokenize(["What you know you can't explain, but you feel it."])
# print(subtokens_unicode.to_list())

tokenizer_bert = text.BertTokenizer(filepath, token_out_type=tf.string, lower_case=True)
tokens_bert = tokenizer_bert.tokenize(["What you know you can't explain, but you feel it."])
print(tokens_bert)