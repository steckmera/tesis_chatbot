#!pip install torch transformers datasets accelerate bitsandbytes


from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Cargar el modelo y el tokenizador
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")

# Ensure the entire model is on the same device (GPU if available)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device) 

# Crear una función simple de chatbot
def chat(query):
    inputs = tokenizer(query, return_tensors="pt").to(device) # Move inputs to the same device as the model
    outputs = model.generate(**inputs, max_length=512, do_sample=True, top_k=50, top_p=0.95)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Prueba con un ejemplo de consulta

while True:
  print(".......")
  question = input("Pregunta: ")
  if question == "salir":
    print("Fue un placer, Adios!!!, vuelve pronto")
    break
  print("Respuesta: ")
  print(chat(question))
