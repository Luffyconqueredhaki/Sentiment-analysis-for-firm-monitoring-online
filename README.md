# Progetto MLOps: Sentiment Analysis (Fine-Tuning)

Questo progetto ha due scopi:
1.  **Machine Learning:** Fare il fine-tuning di un modello (RoBERTa) per la Sentiment Analysis di tweet.
2.  **MLOps:** Costruire una pipeline automatica (CI/CD) che testa il codice prima che venga unito.

[![Pipeline CI](https://github.com/Luffyconqueredhaki/Sentiment-analysis-for-firm-monitoring-online/actions/workflows/ci.yml/badge.svg)](https://github.com/Luffyconqueredhaki/Sentiment-analysis-for-firm-monitoring-online/actions/workflows/ci.yml)

---

## 1. Cosa fa il Notebook (`notebooks/`)

Il file `.ipynb` che si trova nella cartella `notebooks/` è il **cervello del progetto di Machine Learning**.

È il file dove è stata fatta tutta la sperimentazione. Il suo compito è:
* **Caricare i Dati:** Scarica e carica il dataset Sentiment140.
* **Fare il Retraining:** Prende il modello `cardiffnlp/twitter-roberta-base-sentiment-latest` e lo **ri-addestra** sul nostro dataset (passando da 3 a 2 etichette: Positivo/Negativo).
* **Valutare:** Calcola le metriche di performance (Accuracy, F1-score) e crea i grafici (come la Confusion Matrix) per dimostrare che il modello funziona.

---

## 2. Cosa fa la Pipeline (e a cosa servono i file)

Questa è la **Fase 2 (MLOps)** che abbiamo costruito. Lo scopo è **testare automaticamente il codice**.

### `.github/workflows/ci.yml`
* **A cosa serve:** Questo è il file che **definisce la pipeline CI**.
* **Cosa fa:** Dà istruzioni a GitHub. Dice: "Ogni volta che Flavio fa un `push`, tu devi fare questo":
    1.  Avviare un server (`runs-on: ubuntu-latest`).
    2.  Installare Python (`Set up Python 3.10`).
    3.  Installare le librerie giuste (leggendo `requirements.txt`).
    4.  Eseguire i test (lanciando `pytest tests/`).

### `requirements.txt`
* **A cosa serve:** È la "lista della spesa" delle librerie Python.
* **Cosa fa:** Garantisce che la pipeline CI (e chiunque altro) usi le **stesse identiche versioni** di `transformers`, `pytest`, `torch`, ecc., per evitare errori.

### `src/preprocessing.py`
* **A cosa serve:** Contiene il codice "pulito" e riutilizzabile.
* **Cosa fa:** Contiene la funzione `preprocess_social` che abbiamo tolto dal notebook. Mettere il codice qui (invece che in un notebook) permette ai test di **importarlo e controllarlo**.

### `tests/test_preprocessing.py`
* **A cosa serve:** È il file dei **test automatici**.
* **Cosa fa:** Questo file **controlla** che la funzione in `src/preprocessing.py` funzioni come deve.
* La pipeline (`ci.yml`) esegue *questo* file. Se tutti i test passano (es. `assert "testo pulito" == "testo pulito"`), la pipeline dà la spunta verde ✅. Se un test fallisce, dà la ❌ rossa e ti avvisa.
