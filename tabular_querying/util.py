import json

import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util
import ifcopenshell.util.element as Element


ifc_entities = {
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
    level = Element.get_container(component)
    if level:
        all_psets_values['Geschoss'] = level.Name

    # get all psets
    psets_content = list(Element.get_psets(component, psets_only=True).values())

    if psets_content:
        for pset in psets_content:
            all_psets_values.update(pset)

    # get all qtos
    qto_content = list(Element.get_psets(component, qtos_only=True).values())

    if qto_content:
        for qto in qto_content:
            all_psets_values.update(qto)

    return all_psets_values


if __name__ == '__main__':
    ifc_model = ifcopenshell.open(".././data_ifc_models/Beispielbüro.ifc")
    components = ifc_model.by_type("IfcElement")
    for component in components:
        if component.is_a().replace('StandardCase', '') in ifc_entities:
            print(get_keyvalues(component))
