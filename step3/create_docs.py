"""Diese Datei ruft die Funktionen auf, welche die synthetischen Dokumente aus dem IFC Modell erzeugen"""

from step3.create_doc.create_doc_metadata import create_doc_metadata
from step3.create_doc.create_doc_elements import create_doc_elements
from step3.create_doc.create_doc_entities import create_doc_entities
from step3.create_doc.create_doc_util import delete_docs


def create_docs(path):
    """Ruft die Funktionen auf, welche die synthetischen Dokumente aus dem IFC Modell erzeugen"""

    # Löscht alle zuvor erstellten Dokumente
    delete_docs()

    # Erstellt ein Dokument zu den Metadaten der IFC-Datei
    create_doc_metadata(path)

    # Erstellt Dokumente für alle Elemente aus der IFC-Datei mit ihren Attributen
    create_doc_elements(path)

    # Erstellt ein Dokument für die Anzahl der Bauteile in der IFC-Datei
    create_doc_entities(path)


if __name__ == '__main__':
    """Testet die Funktionen dieser Datei"""

    path = "../data_ifc_models/Beispielhaus.ifc"
    create_docs(path)
