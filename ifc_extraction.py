import csv
import json

import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util
import ifcopenshell.util.element

ifc_entities = {
    "IfcSlab": "Decke",
    "IfcOpeningElement": "Öffnung",
    "IfcDoor": "Tür",
    "IfcStair": "Treppe",
    "IfcSanitaryTerminal": "Sanitärobjekt",
    "IfcBuildingElementProxy": "Allgemeines Bauteil",
    "IfcFurniture": "Möbel",
    "IfcBuildingElementPart": "Allgemeines Bauteil",
    "IfcWindow": "Fenster",
    "IfcRailing": "Geländer",
    "IfcWall": "Wand",
    "IfcLightFixture": "Licht",
    "IfcCurtainWall": "Vorhangfassade",
    "IfcBeam": "Träger",
    "IfcColumn": "Stütze",
    "IfcMember": "Stabelement",
}


def get_attribute_value_pairs(ifc_path):
    model = ifcopenshell.open(ifc_path)
    components = model.by_type("IfcElement")

    all_properties = []
    for component in components:
        keyvalues = []
        psets_content = list(ifcopenshell.util.element.get_psets(component).values())
        if psets_content:
            component_type = ifc_entities[component.is_a().replace('StandardCase', '')]
            keyvalues.append(('GUID', component.GlobalId))
            keyvalues.append(('IfcType', component.is_a()))
            keyvalues.append(('Bauteiltyp', component_type))
            keyvalues.append(('Name', component.Name))
            keyvalues.append(('Geschoss', ''))
            level = ifcopenshell.util.element.get_container(component)
            if level:
                keyvalues.append(('Geschoss', level.Name))

            for pset in psets_content:
                pset_as_tuple = [(k, v) for k, v in pset.items()]
                keyvalues.extend(pset_as_tuple)
        all_properties.append(dict(keyvalues))
    return all_properties


def convert_to_csv(ifc_path):
    all_properties = get_attribute_value_pairs(ifc_path)
    keys = set()
    for property in all_properties:
        keys.update(property.keys())

    key_list = list(keys)
    print(key_list)

    fieldnames = all_properties[0].keys()

    # Datei im Schreibmodus öffnen und CSV-Writer erstellen
    with open("data/output.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=key_list)

        # Schreiben der Spaltennamen
        writer.writeheader()

        # Schreiben der Datenzeilen
        writer.writerows(all_properties)

    print("CSV-Datei erfolgreich erstellt.")


    # # Open a file to write the attributes to
    # file_name = "data/Attribute_" + ifc_path.split("/")[1].replace("ifc", "txt")
    # output_file = open(file_name, "w", encoding="utf-8")
    #
    # for component in components:
    #     all_psets_values = []
    #     psets_content = list(ifcopenshell.util.element.get_psets(component).values())
    #     if psets_content:
    #         component_type = ifc_entities[component.is_a().replace('StandardCase', '')]
    #         all_psets_values.append(('GUID', component.GlobalId))
    #         all_psets_values.append(('IfcType', component.is_a()))
    #         all_psets_values.append(('Bauteiltyp', component_type))
    #         all_psets_values.append(('Name', component.Name))
    #         all_psets_values.append(('Geschoss', ''))
    #         level = ifcopenshell.util.element.get_container(component)
    #         if level:
    #             all_psets_values.append(('Geschoss', level.Name))
    #
    #         for pset in psets_content:
    #             pset_as_tuple = [(k, v) for k, v in pset.items()]
    #             all_psets_values.extend(pset_as_tuple)
    #         output_file.write(str(dict(all_psets_values)).replace("{", "").replace("}", "") + "\n")
    # print("Attribute wurden in " + file_name + " geschrieben.")
    # return all_psets_values


if __name__ == '__main__':
    output = convert_to_csv("ifc_models/Beispielbüro.ifc")
    print(json.dumps(output, indent=4, ensure_ascii=False))
