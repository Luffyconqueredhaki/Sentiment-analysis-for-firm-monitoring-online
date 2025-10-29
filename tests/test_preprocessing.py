# tests/test_preprocessing.py
from src.preprocessing import preprocess_social

def test_rimozione_mention_url():
    #Testa che @mention e URL siano sostituiti
    testo = "Ciao @amico, guarda https://sito.com"
    atteso = "Ciao @user, guarda http"
    assert preprocess_social(testo) == atteso

def test_gestione_hashtag():
    #Testa che gli hashtag siano gestiti.
    testo = "Adoro #MLOps"
    atteso = "Adoro MLOps"
    assert preprocess_social(testo) == atteso

def test_testo_pulito():
    #Testa un testo che non deve cambiare
    testo = "Un testo normale."
    atteso = "Un testo normale."
    assert preprocess_social(testo) == atteso
