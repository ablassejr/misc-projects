from transformers import AutoTokenizer, AutoModel
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
inputs = tokenizer("Hello World!", return_tensors="pt")
model = AutoModel.from_pretrained("bert-base-uncased")
outputs = model(**inputs)
print(outputs.last_hidden_state.shape)
