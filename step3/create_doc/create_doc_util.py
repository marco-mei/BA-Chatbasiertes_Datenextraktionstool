"""Diese Datei enthält Funktionen, welche die Erstellung der Dokumente unterstützen."""

import json
import ifcopenshell.util.element as element
import ifcopenshell


def get_unit(key):
    """Nimmt einen Key aus dem QTO-Dictionary und gibt die entsprechende Einheit zurück"""

    key = key.lower()
    if any(unit in key for unit in ['height', 'depth', 'width', 'perimeter', 'length', 'thickness']):
        return 'm'
    elif 'area' in key:
        return 'm²'
    elif 'volume' in key:
        return 'm³'
    else:
        return None


def get_qtos(component):
    """Nimmt ein Bauteil und gibt ein Dictionary mit den QTOs und den Einheiten zurück."""

    # Liest alle QTOs aus dem Bauteil aus
    qto_dict = {}
    qto_content = element.get_psets(component, qtos_only=True).values()

    # Erstellt ein Dictionary mit den QTOs und den Einheiten und filtert nicht relevante Attribute heraus
    for qto in qto_content:
        qto_dict.update({key: f"{round(value, 2)} {get_unit(key)}" for key, value in qto.items() if not isinstance(value, dict) and not key == 'id'})

    # Gibt das Dictionary zurück
    return qto_dict


def get_psets(component):
    """Nimmt ein Bauteil und gibt ein Dictionary mit den Psets und den Werten zurück."""

    # Liest alle Psets aus dem Bauteil aus
    pset_dict = {}
    pset_content = element.get_psets(component, psets_only=True).values()

    # Erstellt ein Dictionary mit den Psets und den Werten und filtert nicht relevante Attribute heraus
    for pset in pset_content:
        pset_dict.update({key: value for key, value in pset.items() if not isinstance(value, (list, dict)) and not key == 'id' and not value == ''})

    # Gibt das Dictionary zurück
    return pset_dict


def delete_docs():
    """Löscht die Dokumente aus dem Ordner"""

    import os
    import shutil
    if os.path.exists('../docs_data'):
        shutil.rmtree('../docs_data')


if __name__ == '__main__':
    """Testet die Funktionen"""

    ifc = ifcopenshell.open("../../data_ifc_models/Beispielhaus.ifc")
    components = ifc.by_type("IfcRoot")
    for component in components:
        print(json.dumps(get_psets(component), indent=4, ensure_ascii=False)) if get_qtos(component) else None
