from step3.create_doc.create_doc_metadata import create_doc_metadata


def create_docs(path):
    create_doc_metadata(path)


if __name__ == '__main__':
    path = "../data_ifc_models/Beispielhaus.ifc"
    create_docs(path)
