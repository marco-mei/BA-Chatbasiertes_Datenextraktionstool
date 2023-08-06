import json
from step1.startLanguageModel import startLanguageModel, generateAnswer

with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)


def evaluateStep1():
    def startModel(path, question, chain):
        result = generateAnswer(path, question['question'], chain)
        print(f"Frage {question['id']}: {question['question']}:")
        print(f"{result}")
        print("=====================================")

    path = "../BA-Chatbasiertes_Datenextraktionstool/data_ifc_models/Beispielhaus.ifc"
    chain = startLanguageModel(path)

    for question in questions:
        startModel(path, question, chain)


if __name__ == '__main__':
    evaluateStep1()
