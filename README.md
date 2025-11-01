# Progetto MLOps: Sentiment Analysis (Fine-Tuning RoBERTa)

Questo repository contiene un progetto completo di MLOps per l'analisi del sentiment dei social media (es. Twitter/X). Il progetto gestisce l'intero ciclo di vita del modello: dall'addestramento e fine-tuning di un modello Transformer (RoBERTa) fino alla pipeline CI/CD per i test automatici e al monitoring continuo.

## 🎯 Descrizione del Progetto e Casi d'Uso

Questo progetto analizza il sentiment sui social media per monitorare la reputazione online. Il cuore del sistema è un modello **Transformer (RoBERTa)** (`cardiffnlp/twitter-roberta-base-sentiment-latest`), specializzato nel comprendere le sfumature del linguaggio social.

Il modello base, che classifica in 3 classi (Positivo, Neutro, Negativo), viene **ri-addestrato (fine-tuning)** sul dataset Sentiment140 per specializzarlo ulteriormente e adattarlo a 2 sole classi (Positivo/Negativo).

L'intero ciclo di vita del modello è gestito tramite un **flusso MLOps completo**, che include l'addestramento, il test automatico (CI/CD) e il monitoraggio continuo delle performance.

### Casi d'Uso Principali

* **Brand Reputation Management:** Tracciare in tempo reale la percezione pubblica (positiva o negativa) di un'azienda o di un prodotto.
* **Analisi del Feedback Cliente:** Estrarre insight azionabili da migliaia di recensioni di prodotti, app (App Store, Play Store) o servizi.
* **Market Research:** Comprendere l'opinione pubblica su specifici argomenti, trend di settore o sui competitor.
* **Monitoraggio Campagne:** Valutare l'impatto e la ricezione (positiva o negativa) di una campagna di marketing o di un evento.

---

## 1. Il Notebook di Sperimentazione (notebooks/)

Il file `.ipynb` nella cartella `notebooks/` è il **cervello del progetto di Machine Learning**. È dove è stata fatta tutta la sperimentazione.

* **Caricare i Dati:** Scarica e carica il dataset Sentiment140.
* **Fare il Retraining (Fine-Tuning):** Prende il modello `cardiffnlp/twitter-roberta-base-sentiment-latest` e lo ri-addestra sul nostro dataset, passando da 3 a 2 etichette (Positivo/Negativo).
* **Valutare:** Calcola le metriche di performance (Accuracy, F1-score) e crea i grafici (come la Confusion Matrix) per dimostrare che il modello funziona.

---

## 2. La Pipeline di Test (CI)

Questa è la **Fase 2 (MLOps)**. Lo scopo è **testare automaticamente il codice** prima che venga unito al ramo principale (es. `main`).

### .github/workflows/ci.yml

* **A cosa serve:** Questo è il file che **definisce la pipeline CI (Continuous Integration)**.
* **Cosa fa:** Dà istruzioni a GitHub. Dice: "Ogni volta che qualcuno fa un *push*, tu devi":
    1.  Avviare un server (`runs-on: ubuntu-latest`).
    2.  Installare Python (`Set up Python 3.10`).
    3.  Installare le librerie giuste (leggendo `requirements.txt`).
    4.  Eseguire i test (lanciando `pytest tests/`).

### requirements.txt

* **A cosa serve:** È la "lista della spesa" delle librerie Python.
* **Cosa fa:** Garantisce che la pipeline CI (e chiunque altro) usi le **stesse identiche versioni** di `transformers`, `pytest`, `torch`, ecc., per evitare errori di compatibilità.

### src/preprocessing.py

* **A cosa serve:** Contiene il codice "pulito", testabile e riutilizzabile.
* **Cosa fa:** Contiene la funzione `preprocess_social` (estratta dal notebook). Mettere il codice qui (invece che in un notebook) permette ai test di importarlo e controllarlo.

### tests/test_preprocessing.py

* **A cosa serve:** È il file dei **test automatici (unit test)**.
* **Cosa fa:** Questo file **controlla** che la funzione in `src/preprocessing.py` funzioni come ci si aspetta. La pipeline (`ci.yml`) esegue questo file.
    * Se tutti i test passano (es. `assert "testo pulito" == "testo pulito"`), la pipeline dà la **spunta verde ✅**.
    * Se un test fallisce, dà la **❌ rossa** e blocca l'unione (merge) del codice.

---

## 3. Il Monitoring (Model & Data Drift)

Questa è la **Fase 3 (MLOps)**. Dopo che il modello è stato rilasciato (deploy), dobbiamo assicurarci che continui a funzionare bene nel mondo reale. Il monitoring serve a **rilevare il degrado del modello (model decay)** e il cambiamento dei dati (data drift).

*(Nota: I file seguenti sono esempi concettuali di come il monitoring viene implementato)*

### monitoring/check_drift.py (Esempio)

* **A cosa serve:** Rileva il **Data Drift** (il cambiamento dei dati nel tempo).
* **Cosa fa:** Questo script confronta statisticamente i nuovi dati in arrivo (es. i tweet della scorsa settimana) con i dati su cui il modello è stato addestrato (il *training set*). Se i nuovi dati sono troppo "diversi" (es. usano nuovo slang, parlano di argomenti imprevisti), il modello potrebbe non essere più accurato. Questo script lancia un allarme, segnalando che è ora di un *retraining*.

### monitoring/dashboard.py (Esempio con Streamlit/Dash)

* **A cosa serve:** È la dashboard di controllo visiva per monitorare la salute del modello.
* **Cosa fa:** Mostra le metriche chiave in tempo reale:
    * **Performance del Modello:** Monitora l'accuracy o l'F1-score (se abbiamo nuovi dati etichettati) per identificare il **Model Drift**.
    * **Distribuzione delle Predizioni:** Quanti tweet positivi vs. negativi stiamo vedendo? (Un picco improvviso di negatività è un segnale di business importante).
    * **Stato del Servizio (Health):** L'endpoint del modello risponde? Quanti errori? Qual è la latenza?

### .github/workflows/monitor.yml (Esempio)

* **A cosa serve:** Automatizza i controlli di monitoring a intervalli regolari.
* **Cosa fa:** È una pipeline (GitHub Action) che gira in modo schedulato (es. ogni notte) ed esegue lo script `check_drift.py`. Se rileva un drift significativo, può automaticamente aprire una *Issue* su GitHub o inviare una notifica Slack al team MLOps.
