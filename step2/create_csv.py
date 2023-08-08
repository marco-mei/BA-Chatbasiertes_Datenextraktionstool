import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util
from util import get_keyvalues, ifc_entities


def create_csv(path):
    # Öffnet das IFC Modell
    ifc_model = ifcopenshell.open(path)

    # Erstellt eine Liste mit allen Komponenten mit der Superklasse IFCElement
    components = [component for component in ifc_model.by_type("IfcRoot") if component.is_a().replace('StandardCase', '') in ifc_entities]
    column_names = []

    # Iteriert über alle Komponenten und fügt alle Attributnamen zu einer Liste hinzu
    for component in components:
        column_names.extend(list(get_keyvalues(component).keys()))

    # Entfernt Duplikate und sortiert die Spaltennamen
    column_names = list(set(column_names))
    column_names.sort()

    # save column names to csv file
    with open(r"C:\Users\meine\PycharmProjects\BA-Chatbasiertes_Datenextraktionstool\step2\csv_data\CSV_Data.csv", "w", encoding="utf-8") as f:
        # Schreibt alle Spaltennamen in die CSV Datei
        f.write(",".join(column_names))

        # Schreibt einen Zeilenumbruch in die CSV Datei
        f.write("\n")  # Write newline after column names

        # Iteriert über alle Komponenten
        for component in components:

            # Generiert ein Dictionary mit allen key-value Paaren
            keyvalues = get_keyvalues(component)

            # Liest die Werte zu den Spaltennamen für die Komponente aus und speichert sie in einer Liste
            row_values = [str(keyvalues.get(column, "")) for column in column_names]

            # Schreibt die Werte in die CSV Datei
            f.write(",".join(row_values))

            # Schreibt einen Zeilenumbruch in die CSV Datei
            f.write("\n")

    print(f"\nSingle CSV with {len(column_names)} columns has been created")


# if __name__ == '__main__':
#     create_csv("../data_ifc_models/Beispielhaus.ifc")


if __name__ == '__main__':
    path = r"C:\Users\meine\PycharmProjects\BA-Chatbasiertes_Datenextraktionstool\data_ifc_models\Beispielhaus.ifc"
    ifc = ifcopenshell.open(path)
    # get metadata of ifc
    print(ifc.get_application())
