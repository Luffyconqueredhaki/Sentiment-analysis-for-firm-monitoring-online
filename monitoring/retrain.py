from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments
from datasets import load_dataset
import torch

MODEL_PATH = "model/"
NEW_MODEL_OUTPUT = "model/"

def main():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

    dataset = load_dataset("csv", data_files="monitoring/data/new_data.csv")

    def tokenize(batch):
        return tokenizer(batch["text"], truncation=True, padding=True)

    dataset = dataset.map(tokenize, batched=True)

    training_args = TrainingArguments(
        output_dir=NEW_MODEL_OUTPUT,
        num_train_epochs=1,
        per_device_train_batch_size=8,
        save_strategy="epoch",
        logging_steps=10
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset["train"]
    )

    trainer.train()
    model.save_pretrained(NEW_MODEL_OUTPUT)
    tokenizer.save_pretrained(NEW_MODEL_OUTPUT)

if __name__ == "__main__":
    main()
