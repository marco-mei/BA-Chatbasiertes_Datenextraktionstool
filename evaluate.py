import json
from step1.initialize_model_step1 import get_chain as get_chain1
from step1.initialize_model_step1 import generateAnswer as generateAnswer1
from step2.initialize_model_step2 import get_chain as get_chain2
from step2.initialize_model_step2 import generateAnswer as generateAnswer2
from step2.create_csv import create_csv

with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

path = "data_ifc_models/Beispielhaus.ifc"


def evaluateStep1():
    def getAnswer(path, query, chain):
        result = generateAnswer1(path, query['question'], chain)
        print(f"Frage {query['id']}: {query['question']}:")
        print(f"{result}")
        print("=====================================")

    chain = get_chain1(path)

    for question in questions:
        getAnswer(path, question, chain)


def evaluateStep2():
    def getAnswer(path, query, chain):
        result = generateAnswer2(path, query['question'], chain)
        print(f"Frage {query['id']}: {query['question']}:")
        print(f"{result}")
        print("=====================================")

    # Erstelle csv-Datei aus Ifc-Modell
    create_csv(path)

    chain = get_chain2(path)

    for question in questions:
        getAnswer(path, question, chain)


if __name__ == '__main__':
    evaluateStep2()
