from langchain.chains import RetrievalQA
from langchain.document_loaders import CSVLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.llms import OpenAI
import os


def execute_model(path):
    os.environ["OPENAI_API_KEY"] = "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"

    # Load the documents using pandas
    loader = CSVLoader(file_path=path)

    # Create an index using the loaded documents
    index_creator = VectorstoreIndexCreator()
    docsearch = index_creator.from_loaders([loader])

    # Create a question-answering chain using the index
    chain = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=docsearch.vectorstore.as_retriever(), input_key="question")

    # Pass a query to the chain
    query = "Wie viele Türen sind im Modell?"
    response = chain({"question": query})

    print(response['result'])


if __name__ == '__main__':
    path = ".././data_single_csv/Model_Attributes.csv"
    execute_model(path)
