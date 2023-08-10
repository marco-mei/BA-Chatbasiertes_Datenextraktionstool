"""Enthält Utility-Funktionen für die Verarbeitung von IFC-Dateien."""

import ifcopenshell.util.element as element

# Liste der relevanten IFC-Entitäten mit deutscher Übersetzung
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
    """Gibt alle Pset- und Qto-Werte eines Bauteils zurück."""

    # Erstellt ein Dictionary mit allen IFC-Attributen des Bauteils
    all_psets_values = {'GUID': component.GlobalId, 'IfcType': component.is_a()}

    # Fügt den Bauteiltypen hinzu, falls dieser in der Liste der relevanten IFC-Entitäten enthalten ist
    if component.is_a().replace('StandardCase', '') in ifc_entities:
        component_type = ifc_entities[component.is_a().replace('StandardCase', '')]
        all_psets_values['Bauteiltyp'] = component_type
    else:
        all_psets_values['Bauteiltyp'] = ''

    # Fügt den Bauteilnamen und das Geschoss hinzu
    all_psets_values['Name'] = component.Name
    all_psets_values['Geschoss'] = ''
    level = element.get_container(component)
    if level:
        all_psets_values['Geschoss'] = level.Name

    # Generiert eine Liste aller Pset-Werte und fügt diese in eine Liste ein
    psets_content = list(element.get_psets(component, psets_only=True).values())

    if psets_content:
        for pset in psets_content:
            all_psets_values.update(pset)

    # Generiert eine Liste aller Qto-Werte und fügt diese in eine Liste ein
    qto_content = list(element.get_psets(component, qtos_only=True).values())

    if qto_content:
        for qto in qto_content:
            all_psets_values.update(qto)

    # Löscht alle Einträge aus der Liste, die ein Dictionary enthalten
    del_items = []
    for key in all_psets_values:
        value = all_psets_values[key]
        if type(value) == dict:
            del_items.append(key)
    for item in del_items:
        del all_psets_values[item]

    # Gibt das Dictionary mit den IFC-Attributen, sowie den bereinigten Pset- und Qto-Werten zurück
    return all_psets_values
