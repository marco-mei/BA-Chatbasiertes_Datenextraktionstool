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

    # Open a file to write the attributes to
    file_name = "data/Attribute_" + ifc_path.split("/")[1].replace("ifc", "txt")
    output_file = open(file_name, "w", encoding="utf-8")

    for component in components:
        all_psets_values = []
        psets_content = list(ifcopenshell.util.element.get_psets(component).values())
        if psets_content:
            component_type = ifc_entities[component.is_a().replace('StandardCase', '')]
            all_psets_values.append(('GUID', component.GlobalId))
            all_psets_values.append(('IfcType', component.is_a()))
            all_psets_values.append(('Bauteiltyp', component_type))
            all_psets_values.append(('Name', component.Name))
            all_psets_values.append(('Geschoss', ''))
            level = ifcopenshell.util.element.get_container(component)
            if level:
                all_psets_values.append(('Geschoss', level.Name))

            for pset in psets_content:
                pset_as_tuple = [(k, v) for k, v in pset.items()]
                all_psets_values.extend(pset_as_tuple)
            output_file.write(str(dict(all_psets_values)).replace("{", "").replace("}", "") + "\n")
    print("Attribute wurden in " + file_name + " geschrieben.")


if __name__ == '__main__':
    print(get_attribute_value_pairs("ifc_models/AC20-FZK-Haus.ifc"))