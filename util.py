import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util
import ifcopenshell.util.element


ifc_entities = {
    "IfcSlab": "Decke",
    "IfcOpeningElement": "Öffnung",
    "IfcDoor": "Tür",
    "IfcStair": "Treppe",
    "IfcSanitaryTerminal": "Sanitärbauteil",
    "IfcBuildingElementProxy": "Allgemeines Bauteil",
    "IfcFurniture": "Möbel",
    "IfcBuildingElementPart": "Allgemeines Bauteil",
    "IfcWindow": "Fenster",
    "IfcRailing": "Geländer",
    "IfcWall": "Wand",
    "IfcLightFixture": "Licht",
    "IfcCurtainWall": "Vorhangfassade"
}


def get_keyvalues(ifc_element):
    psets = ifcopenshell.util.element.get_psets(ifc_element).values()
    for pset in psets:
        keyvalues = ifcopenshell.util.element.get_pset_values(ifc_element, pset)
    return keyvalues


def get_ifc_elements(ifc_model):
    elements = ifc_model.by_type("IfcElement")
    ifc_entities = []
    for element in elements:
        ifc_entities.append(element.is_a())
    return list(set(ifc_entities))


def get_number_of_elements(ifc_model, ifc_entity=None):
    return len(ifc_model.by_type(ifc_entity))


def get_number_of_all_entities(ifc_file):
    ifc_model = ifcopenshell.open(ifc_file)
    ifc_entities = get_ifc_elements(ifc_model)
    for entity in ifc_entities:
        if entity is not None:
            entity_amount = get_number_of_elements(ifc_model, entity)
            print(f"{entity}: {entity_amount}")


def test_function(ifc_file):
    ifc_model = ifcopenshell.open(ifc_file)
    doors = ifc_model.by_type("IfcDoor")
    for door in doors:
        print(get_keyvalues(door))


def get_all_attributes(ifc_file):
    ifc_model = ifcopenshell.open(ifc_file)
    ifc_entities = get_ifc_elements(ifc_model)
    output_file = open("component_attributes.txt", "w")
    for entity in ifc_entities:
        if entity is not None:
            elements = ifc_model.by_type(entity)
            for element in elements:
                output_file.write(entity + "\n")
                output_file.write(get_keyvalues(element) + "\n")
                keyvalues = ifcopenshell.util.element.get_psets(element)


def create_attribute_file(ifc_file):
    print("test")


if __name__ == "__main__":
    print(get_number_of_all_entities("ifc_models/AC20-FZK-Haus.ifc"))
    print(test_function("ifc_models/Beispielbüro.ifc"))
