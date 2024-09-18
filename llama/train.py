#!pip install torch transformers datasets accelerate bitsandbytes peft
#!env PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model
import torch
from datasets import Dataset

# Cargar el dataset desde un archivo CSV
dataset = Dataset.from_dict({
     "inputs": ["Hola", "¿Cómo te llamas?", "¿Qué tal?", "Dame informacion sobre admisiones","Dame los requisitos","Horarios de atención","Chao","Adios"],
     "outputs": ["Hola!", "Soy un chatbot.", "Estoy bien, gracias.", "Nuestro periodo de admisiones inicial el 15 de octubre","los requisitos son: copia de cedula, foto carnet y cancelar $30 dolares","Nuestros horarios de atención son de Lunes a viernes de 8am hasta las 4pm","Fue un placer atenderte, Adios!!!","Chao que tengas un gran día"]
 })


# Cargar el modelo y el tokenizador
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
tokenizer.pad_token = tokenizer.eos_token

# Ensure the entire model is on the same device (GPU if available)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device) 

lora_config = LoraConfig(
     r=16,
     lora_alpha=32,
     lora_dropout=0.05,
     bias="none",
     task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()


def train_function(examples):
    inputs = tokenizer(examples["inputs"], return_tensors="pt", padding="max_length", truncation=True, max_length=512)
    outputs = tokenizer(examples["outputs"], return_tensors="pt", padding="max_length", truncation=True, max_length=512)
    return {"input_ids": inputs.input_ids, "attention_mask": inputs.attention_mask, "labels": outputs.input_ids}

tokenized_dataset = dataset.map(train_function, batched=True)

training_args = TrainingArguments(
    output_dir="./results",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    learning_rate=2e-5,
    num_train_epochs=1,
    fp16=True,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
)

trainer.train()

trainer.save_model("./drive/MyDrive/UEES/my_fine_tuned_llama")
tokenizer.save_pretrained("./drive/MyDrive/UEES/my_fine_tuned_llama")