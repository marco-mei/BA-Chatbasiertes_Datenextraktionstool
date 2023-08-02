import json
import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util
import ifcopenshell.util.element as Element

from util import get_keyvalues, ifc_entities


def create_multiple_csv(path):
    ifc_model = ifcopenshell.open(path)
    components = ifc_model.by_type("IfcElement")
    model_entities = list(set([component.is_a() for component in components if component.is_a().replace('StandardCase', '') in ifc_entities]))

    for model_entity in model_entities:
        column_names = []
        entity_components = ifc_model.by_type(model_entity)
        for entity_component in entity_components:
            column_names.extend(list(get_keyvalues(entity_component).keys()))

        column_names = list(set(column_names))
        column_names.sort()

        # save column names to csv file
        with open(f".././data_multiple_csv/{model_entity}_Attributes.csv", "w", encoding="utf-8") as f:
            f.write(",".join(column_names))
            f.write("\n")  # Write newline after column names

            for entity_component in entity_components:
                values = get_keyvalues(entity_component)
                row_values = [str(values.get(column, "")) for column in column_names]
                for row_value in row_values:
                    if row_value == "None":
                        row_value = ""
                f.write(",".join(row_values))
                f.write("\n")

    print(f"\nMultiple CSV have been created for {len(model_entities)} entities")


def create_single_csv(path):
    ifc_model = ifcopenshell.open(path)
    components = [component for component in ifc_model.by_type("IfcElement") if component.is_a().replace('StandardCase', '') in ifc_entities]
    column_names = []

    for component in components:
        column_names.extend(list(get_keyvalues(component).keys()))

    column_names = list(set(column_names))
    column_names.sort()

    # save column names to csv file
    with open(f".././data_single_csv/Model_Attributes.csv", "w", encoding="utf-8") as f:
        f.write(",".join(column_names))
        f.write("\n")  # Write newline after column names

        for component in components:
            values = get_keyvalues(component)
            row_values = [str(values.get(column, "")) for column in column_names]

            for row_value in row_values:
                if "," in row_value:
                    row_values.remove(row_value)
            f.write(",".join(row_values))
            f.write("\n")

    print(f"\nSingle CSV with {len(column_names)} columns has been created")


if __name__ == '__main__':
    create_single_csv(".././data_ifc_models/Beispielbüro.ifc")


if __name__ == '__main__':
    create_multiple_csv(".././data_ifc_models/Beispielbüro.ifc")
