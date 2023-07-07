from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.chat_models import AzureChatOpenAI, ChatOpenAI
from langchain.document_loaders import CSVLoader, DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.llms import OpenAI, OpenAIChat
import os


def execute_model(path, query):
    os.environ["OPENAI_API_KEY"] = "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"

    # Load the documents using pandas
    doc_path = ".././data_multiple_csv/IfcWall_Attributes.csv"
    loader = CSVLoader(file_path=doc_path)
    # # loader = DirectoryLoader('../', glob="**/*.md")
    # loader = DirectoryLoader('.././data', glob='**/*.csv')
    # docs = loader.load()
    # print(docs)

    # Create an index using the loaded documents
    index_creator = VectorstoreIndexCreator()
    docsearch = index_creator.from_loaders([loader])

    # Prompt template
    prompt_template = """Given the following csv file that contains information about a building information model with filetype
            ifc and a question, create a final answer. Every row in the file describes a building element and every row
            consists of attributes and model information about the building element. The file is encoded in UTF-8.
            If you don't know the answer, just say that you don't know. Don't try to make up an answer.
            Respond in German.
            
            {context}
            
            QUESTION: {question}
            =========
            FINAL ANSWER IN German:"""

    # Create a prompt using the template
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    # Prompt kwargs
    chain_type_kwargs = {"prompt": prompt}

    # Define document name as context
    context = "CONTEXT: " + path.split("/")[-1].split(".")[0]

    # Create a question-answering chain using the index
    llm = ChatOpenAI(model_name='gpt-3.5-turbo')
    chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.vectorstore.as_retriever(), chain_type_kwargs=chain_type_kwargs)

    # Pass a query to the chain
    response = chain({"query": query, "context": context})
    return response['result']


if __name__ == '__main__':
    path = ".././data_single_csv/Model_Attributes.csv"
    # path = ".././data_multiple_csv/IfcCurtainWall_Attributes.csv"
    execute_model(path, "Wie viele Vorhangfassaden sind im Modell?")
