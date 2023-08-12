"""Diese Datei erstellt ein Dokument mit den Anzahlen der Bauteile zu dem IFC-Modell."""

from util import ifc_entities
import ifcopenshell


def create_entity_json(path):
    """Nimmt den Pfad zur IFC-Datei und gibt ein Dictionary zurück, welches alle Entitäten aus dem Modell enthält."""

    # Öffne die IFC-Datei
    ifc = ifcopenshell.open(path)

    # Erstellt ein Dictionary mit allen IFC-Entitäten der Superklasse IfcRoot und deren Anzahl im Modell
    components = ifc.by_type("IfcRoot")
    entity_dict = {}
    for component in components:
        if component.is_a() in ifc_entities:
            if component.is_a() not in entity_dict:
                entity_dict[component.is_a()] = 1
            else:
                entity_dict[component.is_a()] += 1
    return entity_dict


def create_doc_entities(path):
    """Diese Funktion erstellt ein Dokument mit den Anzahlen der Bauteile zu dem IFC-Modell."""

    # Erzeugt ein Dictionary mit den Anzahlen der Bauteile
    entity_json = create_entity_json(path)

    # Erstellt ein Dokument mit den Anzahlen der Bauteile zu dem IFC-Modell
    with open(r"C:\Users\meine\PycharmProjects\BA-Chatbasiertes_Datenextraktionstool\step3\docs_data\Bauteilliste_Anzahl.txt", 'w', encoding='utf-8') as file:
        file.write(f"Bauteilliste_Anzahl\n\n")
        file.write(f"Diese Liste enthält die Anzahl aller Bauteile, die in der IFC-Datei vorkommen.\n\n")
        for entity in entity_json:
            file.write(f"{ifc_entities[entity]}: {entity_json[entity]}\n")


if __name__ == '__main__':
    """Testet die Funktion"""

    path = "../../data_ifc_models/Beispielhaus.ifc"
    create_doc_entities(path)
