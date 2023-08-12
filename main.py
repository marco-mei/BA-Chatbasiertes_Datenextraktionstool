"""Diese Datei enthält die Funktion, welche den Chatbot startet."""

import os
import ifcopenshell
import openai

from step1.initialize_model_step1 import get_chain as get_chain1
from step2.initialize_model_step2 import get_chain as get_chain2
from step3.initialize_model_step3 import get_chain as get_chain3
from step3.create_docs import create_docs
from step2.create_csv import create_csv


def start_chatbox():
    """Diese Funktion startet den Chatbot."""
    def get_openai_key():
        """Diese Funktion fragt den OpenAI API Key ab und überprüft diesen."""

        print("Zum Starten des Chatbots wird ein OpenAI API Key benötigt. Bitte geben Sie diesen ein.")
        key = input("Nutzer: ")
        if key.lower() == "exit":
            return

        def is_api_key_valid(key):
            """Diese Funktion überprüft ob der API Key gültig ist."""
            openai.api_key = key
            try:
                response = openai.Completion.create(
                    engine="text-embedding-ada-002",
                    prompt="This is a test.",
                    max_tokens=5
                )
                return True
            except:
                return False

        if not is_api_key_valid(key):
            print("Der API Key ist ungültig. Sie können einen API Key unter https://beta.openai.com/account/api-keys erstellen.\n")
            return get_openai_key()
        elif is_api_key_valid(key):
            return key

    openai_key = get_openai_key()
    os.environ['OPENAI_API_KEY'] = openai_key

    def get_path():
        """Diese Funktion fragt den Pfad der IFC-Datei ab und überprüft diesen."""

        print("\n"+r"Bitte geben Sie den Pfad ihrer IFC-Datei an (z.B.: C:\Users\meine\Downloads\Beispielhaus.ifc).")
        path = rf"{input('Nutzer: ')}"
        if path.lower() == "exit":
            return

        try:
            ifcopenshell.open(path)
            pass

        except:
            print("Die Datei konnte nicht geöffnet werden. Bitte geben Sie einen gültigen Pfad an.\n")
            return get_path()

        return path

    path = get_path()

    def get_step():
        """Diese Funktion fragt die Stufe des Chatbots ab und überprüft diese."""

        print("\nBitte geben Sie an welche Stufe des Chatbots Sie nutzen möchten (1 / 2 / 3 / ?).")
        stepInput = input("Nutzer: ")
        if stepInput.lower() == "exit":
            return
        elif stepInput == "?":
            print("Stufe 1: IFC-Datei als Embedding\n"
                  "Stufe 2: CSV-Tabelle mit Bauteilinformationen als Embedding\n"
                  "Stufe 3: Synthetische Dokumente mit Bauteilinformationen als Embedding\n")
            return get_step()
        elif stepInput not in ["1", "2", "3"]:
            print("Bitte geben Sie eine gültige Stufe an.\n")
            return get_step()
        else:
            print("Das Sprachmodell wird nun initialisiert.")
            return int(stepInput)

    step = get_step()

    def init_model(step, path):
        """Diese Funktion initialisiert das Sprachmodell und erstellt eine Chain."""
        if step == 1:
            return get_chain1(path)
        elif step == 2:
            create_csv(path)
            return get_chain2(path)
        elif step == 3:
            create_docs(path)
            return get_chain3()
        else:
            return None

    chain = init_model(step, path)

    context = path.split("/")[-1].split(".")[0]

    while True:
        """Diese Schleife startet den Chatbot."""

        print("\nBitte geben Sie eine Frage ein (exit zum Beenden).")
        query = input("Nutzer: ")
        if query.lower() == "exit":
            break
        else:
            response = chain({"query": query, "context": context})
            print(response['result']+"\n")


if __name__ == '__main__':
    start_chatbox()
