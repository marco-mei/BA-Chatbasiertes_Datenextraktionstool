from openai_tabular_data_query import execute_model


def start_chatbot(path):
    print("Willkommen beim Chatbot. Bitte geben Sie Ihre Frage ein.\n")
    while True:
        user_input = input("Frage: ")
        if user_input.lower() == "exit":
            break
        else:
            print(execute_model(path, query=user_input))


if __name__ == '__main__':
    start_chatbot("../step2/data_single_csv/Model_Attributes.csv")
