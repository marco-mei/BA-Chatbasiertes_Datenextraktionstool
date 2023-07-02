from create_csv import create_single_csv, create_multiple_csv
from openai_tabular_data_query import execute_model


def main(path, mode):
    if mode == "single":
        create_single_csv(path)
        execute_model(".././data_single_csv/Model_Attributes.csv")
    elif mode == "multiple":
        create_multiple_csv(path)


if __name__ == '__main__':
    main(".././data_ifc_models/Beispielbüro.ifc", "single")
