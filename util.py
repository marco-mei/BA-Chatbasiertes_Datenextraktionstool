import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util
import ifcopenshell.util.element as element

ifc_entities = {
    "IfcProject": "Projekt",
    "IfcSite": "Grundstück",
    "IfcBuilding": "Gebäude",
    "IfcBuildingStorey": "Geschoss",
    "IfcSpace": "Raum",
    "IfcSlab": "Decke",
    "IfcOpeningElement": "Öffnung",
    "IfcDoor": "Tür",
    "IfcStair": "Treppe",
    "IfcSanitaryTerminal": "Sanitärobjekt",
    "IfcBuildingElementProxy": "Allgemeines Bauteil",
    "IfcFurniture": "Möbel",
    "IfcWindow": "Fenster",
    "IfcRailing": "Geländer",
    "IfcWall": "Wand",
    "IfcLightFixture": "Licht",
    "IfcCurtainWall": "Vorhangfassade",
    "IfcBeam": "Träger",
    "IfcColumn": "Stütze",
    "IfcMember": "Stabelement",
}


def get_keyvalues(component):
    all_psets_values = {}

    all_psets_values['GUID'] = component.GlobalId
    all_psets_values['IfcType'] = component.is_a()

    if component.is_a().replace('StandardCase', '') in ifc_entities:
        component_type = ifc_entities[component.is_a().replace('StandardCase', '')]
        all_psets_values['Bauteiltyp'] = component_type

    else:
        all_psets_values['Bauteiltyp'] = ''

    all_psets_values['Name'] = component.Name
    all_psets_values['Geschoss'] = ''
    level = element.get_container(component)
    if level:
        all_psets_values['Geschoss'] = level.Name

    # get all psets
    psets_content = list(element.get_psets(component, psets_only=True).values())

    if psets_content:
        for pset in psets_content:
            all_psets_values.update(pset)

    # get all qtos
    qto_content = list(element.get_psets(component, qtos_only=True).values())

    if qto_content:
        for qto in qto_content:
            all_psets_values.update(qto)

    del_items = []
    for key in all_psets_values:
        value = all_psets_values[key]
        if type(value) == dict:
            del_items.append(key)
    for item in del_items:
        del all_psets_values[item]

    return all_psets_values


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


if __name__ == "__main__":
    path = "data_ifc_models/Beispielhaus.ifc"
    ifc = ifcopenshell.open(path)
    components = ifc.by_type("IfcProduct")
    for component in components:
        print(get_keyvalues(component))
