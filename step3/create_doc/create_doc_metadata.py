import json


def create_doc_metadata(path):
    """Takes path to ifc file and creates metadata file"""

    # Öffnet die IFC-Datei und liest die Zeilen mit den Metadaten aus
    with open(path, "r") as ifc:
        lines = ifc.readlines()
        file_name = lines[2].split(",")

    # Extrahiert die Metadaten aus der IFC-Datei
    def get_model_name():
        return file_name[0].replace("FILE_NAME('", "").replace("'", "").split("\\")[-1].replace(".ifc", "")

    # Extrahiert das Datum aus der IFC-Datei
    def get_date():
        return file_name[1][:11].format("%d.%m.%Y").replace("'", "")

    # Extrahiert die verwendete CAD-Anwendung aus der IFC-Datei
    def get_application():
        return file_name[5].replace("IFC file generated by ", "").replace("'", "").replace(".", "")

    # Extrahiert das vorhandene IFC-Schema aus der IFC-Datei
    def get_file_schema():
        return lines[3].replace("FILE_SCHEMA(('", "").replace("'));", "").replace("\n", "")

    metadata = {
        "Model name": get_model_name(),
        "Date": get_date(),
        "Application": get_application(),
        "IFC schema": get_file_schema()
    }

    # Erstellt eine Textdatei mit den Metadaten
    with open(r"C:\Users\meine\PycharmProjects\BA-Chatbasiertes_Datenextraktionstool\step3\docs_data\metadata.txt", "w") as file:
        file.write("Metadaten zum IFC-Modell:\n\n")
        for key in metadata:
            file.write(f"{key}: {metadata[key]}\n")


if __name__ == '__main__':
    """Testet die Funktion"""

    path = "../../data_ifc_models/Beispielhaus.ifc"
    print(json.dumps(create_doc_metadata(path), indent=4))
