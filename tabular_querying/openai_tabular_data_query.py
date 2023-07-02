from langchain.chains import RetrievalQA
from langchain.document_loaders import CSVLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.llms import OpenAI
import os
import pandas as pd


def execute_model(path):
    os.environ["OPENAI_API_KEY"] = "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"

    # Load the documents
    loader = CSVLoader(file_path=path, encoding="utf-8")

    # Create an index using the loaded documents
    index_creator = VectorstoreIndexCreator()
    docsearch = index_creator.from_loaders([loader])

    # Create a question-answering chain using the index
    chain = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=docsearch.vectorstore.as_retriever(), input_key="question")

    # Pass a query to the chain
    query = "Do you have a column called age?"
    response = chain({"question": query})

    print(response['result'])


if __name__ == '__main__':
    execute_model(".././data_single_csv/Model_Attributes.csv")
