from create_csv import create_single_csv, create_multiple_csv
from openai_tabular_data_query import execute_model
from chatbot import start_chatbot


def main(path, mode):
    if mode == "single":
        create_single_csv(path)
        start_chatbot(path)
    elif mode == "multiple":
        create_multiple_csv(path)
        start_chatbot(path)


if __name__ == '__main__':
    main(".././data_ifc_models/Beispielbüro.ifc", "single")
