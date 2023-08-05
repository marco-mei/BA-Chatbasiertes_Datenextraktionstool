import json
from step1.startLanguageModel import startLanguageModel
import time

with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)


def startModel(path, question):
    result = startLanguageModel(path, question["question"])
    print(f"Frage {question['id']}: {question['question']}:")
    print(f"{result}\n")


def evaluateStep1():
    path = "../BA-Chatbasiertes_Datenextraktionstool/data_ifc_models/Testmodell.ifc"

    # startModel(path, questions[7])

    for question in questions:
        startModel(path, question)
        time.sleep(100)


if __name__ == '__main__':
    evaluateStep1()
