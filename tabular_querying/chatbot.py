from openai_tabular_data_query import execute_model


def start_chatbot(path):
    print("Welcome to the chatbot. Please enter your question.")
    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            break
        else:
            print(execute_model(path, query=user_input))


if __name__ == '__main__':
    start_chatbot(".././data_single_csv/Model_Attributes.csv")