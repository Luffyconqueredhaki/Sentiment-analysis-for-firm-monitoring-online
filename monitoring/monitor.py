import pandas as pd
from transformers import pipeline
from datasets import load_dataset, concatenate_datasets # Assicurati di avere concatenate_datasets
from sklearn.metrics import accuracy_score, f1_score
from datetime import datetime
import os
import sys

# Import preprocessing from src
sys.path.append(".")
from src.preprocessing import preprocess_social

MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
CSV_PATH = "monitoring/metrics.csv"
N_SAMPLES = 30


#Ora è una lista di parole da cercare

COMPANY_KEYWORD = ["happy", "bad", "good", "love"] 
#La funzione ora accetta una lista e usa la logica "OR" prima prendeva solo una parola

def load_fresh_tweets(keywords_list):
    print("Loading English tweets...")
    ds_en = load_dataset("cardiffnlp/tweet_sentiment_multilingual", "english", split="train")
    print("Loading Italian tweets...")
    ds_it = load_dataset("cardiffnlp/tweet_sentiment_multilingual", "italian", split="train")
    
    # Combina i due dataset
    ds = concatenate_datasets([ds_en, ds_it])
    
    df = ds.to_pandas()
    
    # Crea una stringa regex: "happy|bad|good|love"
    # Il simbolo '|' significa 'OR'
    search_terms = "|".join(keywords_list)
    print(f"Filtering for tweets containing: {search_terms}")
    
    # Applica il filtro. regex=True importante
    df = df[df["text"].str.contains(search_terms, case=False, na=False, regex=True)]
    
    if df.empty:
        print(f"Warning: No tweets found containing any of the keywords.")
        return df 
        # DataFrame vuoto
        
    print(f"Found {len(df)} tweets. Sampling {min(N_SAMPLES, len(df))}.")
    return df.sample(min(N_SAMPLES, len(df)))

def convert_label(label):
    # map HF 3-class to binary
    if label == 2: return 1   # positive
    if label == 1: return 0   # neutral
    return 0                  # negative

def map_prediction(pred):
    if pred == "positive": return 1
    return 0

def run_monitoring():
    print("Loading tweets...")
    # Passo l'intera lista alla funzione
    tweets = load_fresh_tweets(COMPANY_KEYWORD)

     #Aggiunto controllo di sicurezza per DataFrame vuoto
    if tweets.empty:
        print("No tweets found. Saving metrics as 0.0 and exiting.")
        acc = 0.0
        f1 = 0.0
    else:
        tweets["clean"] = tweets["text"].apply(preprocess_social)
        tweets["true"] = tweets["label"].apply(convert_label)

        clf = pipeline("sentiment-analysis", model=MODEL)

        print("Running inference...")
        tweets["pred"] = tweets["clean"].apply(lambda x: map_prediction(clf(x)[0]["label"]))

        acc = accuracy_score(tweets["true"], tweets["pred"])
        f1 = f1_score(tweets["true"], tweets["pred"])

    print(f"Accuracy: {acc:.4f}, F1: {f1:.4f}")

    row = pd.DataFrame([{
        "timestamp": datetime.now(),
        "accuracy": acc,
        "f1": f1
    }])

    mode = "a" if os.path.exists(CSV_PATH) else "w"
    header = not os.path.exists(CSV_PATH)

    row.to_csv(CSV_PATH, mode=mode, header=header, index=False)
    print("Metrics saved.")

if __name__ == "__main__":
    run_monitoring()
