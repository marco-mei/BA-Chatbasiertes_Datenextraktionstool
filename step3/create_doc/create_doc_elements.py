"""Diese Datei erstellt die Dokumentation der Bauteile."""

import ifcopenshell
from util import ifc_entities
import ifcopenshell.util.element as element
from step3.create_doc.create_doc_util import get_qtos, get_psets


def create_elements_json(path):
    """Nimmt den Pfad zur IFC-Datei und gibt ein Dictionary zurück, welches alle Bauteile mit ihren Attributen enthält."""

    # Öffne die IFC-Datei
    ifc = ifcopenshell.open(path)

    # Erstellt ein Dictionary mit allen IFC-Entitäten der Superklasse IfcRoot
    components = ifc.by_type("IfcRoot")
    entities = []
    for component in components:
        if component.is_a() in ifc_entities:
            entities.append(component.is_a())
    entities = list(set(entities))
    entity_dict = {}

    # Erstelle ein Dictionary mit allen Bauteilen und ihren Attributen
    for entity in entities:
        entity_name = ifc_entities[entity]
        entity_dict[entity_name] = []
        for component in ifc.by_type(entity):
            entity_dict[entity_name].append({
                'Bauteiltyp': ifc_entities[component.is_a().replace('StandardCase', '')] if component.is_a().replace('StandardCase', '') in ifc_entities else '',
                'Name': component.Name,
                'GUID': component.GlobalId,
                'IfcType': component.is_a()
            })
            if element.get_container(component):
                entity_dict[entity_name][-1].update({'Geschoss': element.get_container(component).Name})

            # Fügt die Psets und Qtos hinzu
            entity_dict[entity_name][-1].update(get_qtos(component))
            entity_dict[entity_name][-1].update(get_psets(component))

    # Gibt das Dictionary zurück
    return entity_dict


def create_doc_elements(path):
    """Diese Funktion erstellt ein Dokument mit den Bauteilen und den Informationen zu dem IFC-Modell."""

    # Erzeugt ein Dictionary mit den Bauteilen und den Informationen
    element_json = create_elements_json(path)

    # Erstellt ein Dokument für jeden Bauteiltypen mit allen Informationen aus dem IFC-Modell
    for component_name, components in element_json.items():
        with open(fr"C:\Users\meine\PycharmProjects\BA-Chatbasiertes_Datenextraktionstool\step3\docs_data\Bauteilliste_{component_name}.txt", 'w', encoding='utf-8') as file:
            file.write(f"Bauteilliste {component_name}\n\n")
            file.write(f"Diese Liste enthält alle Bauteile mit dem Bauteiltyp: {component_name}\n")
            file.write(f"Jeder Absatz beschreibt dabei ein Bauteil.\n")
            file.write(f"Im modell gibt es {len(components)} Bauteile mit dem Bauteiltyp {component_name}.\n\n")
            for component in components:
                for attribute in component:
                    file.write(f"{attribute}: {component[attribute]}\n")
                file.write("\n")


if __name__ == '__main__':
    """Testet die Funktion"""

    create_doc_elements("../../data_ifc_models/Beispielhaus.ifc")
