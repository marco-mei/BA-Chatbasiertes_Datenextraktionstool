from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import CSVLoader
from langchain.indexes import VectorstoreIndexCreator
import os


def get_chain(path):
    os.environ["OPENAI_API_KEY"] = "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"

    # Load the documents using pandas
    doc_path = r"C:\Users\meine\PycharmProjects\BA-Chatbasiertes_Datenextraktionstool\step2\csv_data\CSV_Data.csv"
    loader = CSVLoader(file_path=doc_path, encoding="utf-8")

    # Create an index using the loaded documents
    docsearch = VectorstoreIndexCreator().from_loaders([loader])

    # Prompt template
    prompt_template = """Given the following csv file that contains information about a building information model with filetype
            ifc and a question, create a final answer. Every row in the file describes a building element and every row
            consists of attributes and model information about the building element. The file is encoded in UTF-8.
            Answer detailed and in full sentences. Round all number to two decimal places.
            Below the short answer you should add a long answer that contains more information and reasons for your answer (Max. 2 sentences).

            Respond in German.

            {context}

            QUESTION: {question}
            =========
            FINAL ANSWER IN German:"""

    # Create a prompt using the template
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    # Prompt kwargs
    chain_type_kwargs = {"prompt": prompt}

    # Create a question-answering chain using the index
    llm = ChatOpenAI(model_name='gpt-3.5-turbo')
    chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.vectorstore.as_retriever(), chain_type_kwargs=chain_type_kwargs)

    return chain


def generateAnswer(path, query, chain):
    """Takes a path to an ifc file, a query and a language model and returns an answer to the query."""

    # Define document name as context
    context = "IFC-Modell: " + path.split("/")[-1]

    response = chain({"query": query, "context": context})
    return response['result']


if __name__ == '__main__':
    path = ".././data_ifc_models/Beispielhaus.ifc"
    query = "Wie viele Türen sind im Modell?"
    print(get_chain(path))
