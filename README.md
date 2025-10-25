🎯 Obiettivi

✅ Automazione dell'analisi del sentiment da social media
✅ Monitoraggio continuo della reputazione aziendale
✅ Pipeline CI/CD per deploy automatico
✅ Sistema di retraining automatico del modello

🔧 Tecnologie Utilizzate

Modello: cardiffnlp/twitter-roberta-base-sentiment-latest
Framework: Transformers (Hugging Face)
Deploy: Hugging Face Hub
CI/CD: GitHub Actions
Linguaggio: Python 3.8+

📂 Struttura del Progetto:
Sentiment-analysis-for-firm-monitoring-online/
│
├── 📓 notebooks/
│   └── Progetto-HF-GITHUB-PROAI-MLOPS-OTTAVIANI-FLAVIO-RUBENS.ipynb
│
├── 🐍 src/
│   ├── __init__.py
│   ├── sentiment_analyzer.py      # Classe principale per analisi sentiment
│   ├── data_processor.py           # Preprocessing dei dati
│   └── utils.py                    # Funzioni utility
│
├── 📊 data/
│   └── sample_tweets.csv           # Dataset di esempio
│
├── 🤖 models/
│   └── (modelli salvati localmente)
│
├── 🔧 scripts/
│   ├── deploy_to_hf.py            # Script deploy Hugging Face
│   ├── evaluate_model.py          # Valutazione performance
│   └── monitor_model.py           # Monitoraggio continuo
│
├── ✅ tests/
│   └── test_sentiment_analyzer.py # Unit tests
│
├── ⚙️ .github/
│   └── workflows/
│       └── ci-cd.yml              # Pipeline CI/CD
│
├── 📋 requirements.txt            # Dipendenze Python
├── 🔨 setup.py                    # Setup installazione
├── 📖 README.md                   # Documentazione
└── 🚫 .gitignore                  # File ignorati da Git


# Clone repository
git clone https://github.com/Luffyconqueredhaki/Sentiment-analysis-for-firm-monitoring-online.git
cd Sentiment-analysis-for-firm-monitoring-online

# Installa dipendenze
pip install -r requirements.txt

# Utilizzo base
from src.sentiment_analyzer import SentimentAnalyzer

# Inizializza analyzer
analyzer = SentimentAnalyzer()

# Analizza un testo
text = "MachineInnovators Inc. is the best company ever!"
result = analyzer.analyze(text)
print(result)

🟢 Positive: Sentiment positivo
⚪ Neutral: Sentiment neutro
🔴 Negative: Sentiment negativo

🤗 Modello su Hugging Face
Il modello è disponibile su: FlavioRubensOttaviani/Sentiment-analysis-for-firm-monitoring-online
https://huggingface.co/FlavioRubensOttaviani/Sentiment-analysis-for-firm-monitoring-online

Scelte Progettuali

Modello RoBERTa: Pre-addestrato su Twitter, ideale per social media
Architettura: Sequence classification con 3 classi
Deploy: Hugging Face per facilità di integrazione
CI/CD: GitHub Actions per automazione completa

🧪 Testing
# Esegui i test
python -m pytest tests/

# Test di coverage
pytest --cov=src tests/

👥 Autore
Dr. Flavio Rubens Ottaviani

GitHub: @Luffyconqueredhaki
Hugging Face: @FlavioRubensOttaviani

📄 Licenza
MIT License
🙏 Ringraziamenti

Cardiff NLP per il modello base
Hugging Face per l'infrastruttura
ProfessionAI per la formazione e caso studio
