"""Methoden zur Evaluierung der einzelnen Stufen des Auswertungs-Tools"""

import json
from step1.initialize_model_step1 import get_chain as get_chain1
from step1.initialize_model_step1 import generateAnswer as generateAnswer1
from step2.initialize_model_step2 import get_chain as get_chain2
from step2.initialize_model_step2 import generateAnswer as generateAnswer2
from step3.initialize_model_step3 import get_chain as get_chain3
from step3.initialize_model_step3 import generateAnswer as generateAnswer3
from step3.create_docs import create_docs
from step2.create_csv import create_csv

# Öffnet die Datei questions.json und speichert die Fragen in der Variable questions
with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

# Einstellung um das Testmodell zu ändern
path = "data_IFC_models/Beispielhaus.ifc"


def evaluateStep1():
    """Funktion zum Testen der ersten Stufe des Auswertungs-Tools"""
    def getAnswer(path, query, chain):
        """Funktion welche aus dem Dateipfad, der Frage und der Chain die Antwort generiert und ausgibt"""
        result = generateAnswer1(path, query['question'], chain)
        print(f"Frage {query['id']}: {query['question']}:")
        print(f"{result}")
        print("=====================================")

    # Erstellt die Chain aus dem IFC-Modell und initialisiert das Sprachmodell
    chain = get_chain1(path)

    # Iteriert über alle Fragen und schickt diese an das Sprachmodell um daraus die Antwort zu generieren
    for question in questions:
        getAnswer(path, question, chain)


def evaluateStep2():
    """Funktion zum Testen der zweiten Stufe des Auswertungs-Tools"""
    def getAnswer(path, query, chain):
        """Funktion welche aus dem Dateipfad, der Frage und der Chain die Antwort generiert und ausgibt"""
        result = generateAnswer2(path, query['question'], chain)
        print(f"Frage {query['id']}: {query['question']}:")
        print(f"{result}")
        print("=====================================")

    # Erstellt eine CSV-Datei aus IFC-Modell mit allen Komponenten und ihren Attributen
    create_csv(path)

    # Erstellt die Chain aus der CSV-Datei und initialisiert das Sprachmodell
    chain = get_chain2(path)

    # Iteriert über alle Fragen und schickt diese an das Sprachmodell um daraus die Antwort zu generieren
    for question in questions:
        getAnswer(path, question, chain)


def evaluateStep3():
    """Funktion zum Testen der dritten Stufe des Auswertungs-Tools"""
    def getAnswer(path, query, chain):
        """Funktion welche aus dem Dateipfad, der Frage und der Chain die Antwort generiert und ausgibt"""
        result = generateAnswer3(path, query['question'], chain)
        print(f"Frage {query['id']}: {query['question']}:")
        print(f"{result}")
        print("=====================================")

    # Erstellt synthetische Dokumente aus dem IFC-Modell
    create_docs(path)

    # Erstellt die Chain aus den synthetischen Dokumenten und initialisiert das Sprachmodell
    chain = get_chain3()

    # Iteriert über alle Fragen und schickt diese an das Sprachmodell um daraus die Antwort zu generieren
    for question in questions:
        getAnswer(path, question, chain)


if __name__ == '__main__':
    evaluateStep3()
