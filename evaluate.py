import json
from step1.startLanguageModel import startLanguageModel
import time

with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)


def evaluateStep1():
    path = "../BA-Chatbasiertes_Datenextraktionstool/data_ifc_models/Beispielbüro.ifc"
    for question in questions:
        result = startLanguageModel(path, question["question"])
        print(result)
        time.sleep(20)


if __name__ == '__main__':
    evaluateStep1()
