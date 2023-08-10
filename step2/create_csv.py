"""Diese Datei erstellt eine CSV Datei mit allen Attributen der Komponenten aus dem IFC Modell."""

import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util
from util import get_keyvalues, ifc_entities


def create_csv(path):
    """Erstellt eine CSV Datei mit allen Attributen der Komponenten aus dem IFC Modell."""

    # Öffnet das IFC Modell
    ifc_model = ifcopenshell.open(path)

    # Erstellt eine Liste mit allen Komponenten mit der Superklasse IfcRoot
    components = [component for component in ifc_model.by_type("IfcRoot") if component.is_a().replace('StandardCase', '') in ifc_entities]
    column_names = []

    # Iteriert über alle Komponenten und fügt alle Attributnamen zu einer Liste hinzu
    for component in components:
        column_names.extend(list(get_keyvalues(component).keys()))

    # Entfernt Duplikate und sortiert die Spaltennamen
    column_names = list(set(column_names))
    column_names.sort()

    # Erstellt eine CSV Datei
    with open(r"C:\Users\meine\PycharmProjects\BA-Chatbasiertes_Datenextraktionstool\step2\csv_data\CSV_Data.csv", "w", encoding="utf-8") as f:
        # Schreibt alle Spaltennamen in die CSV Datei
        f.write(",".join(column_names))
        f.write("\n")

        # Iteriert über alle Komponenten
        for component in components:

            # Generiert ein Dictionary mit allen Attributen der Komponente
            keyvalues = get_keyvalues(component)

            # Liest die Werte zu den Spaltennamen für die Komponente aus und speichert sie in einer Liste
            row_values = [str(keyvalues.get(column, "")) for column in column_names]

            # Schreibt die Werte in die CSV Datei
            f.write(",".join(row_values))
            f.write("\n")

    print(f"\nSingle CSV with {len(column_names)} columns has been created")
