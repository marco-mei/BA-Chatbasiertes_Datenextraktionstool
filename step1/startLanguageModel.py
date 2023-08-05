import os
import tiktoken
from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma


def num_tokens_from_string(path) -> int:
    """Returns the number of tokens in a text string."""
    string: str = open(path, "r").read()
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(string))
    return num_tokens


def startLanguageModel(path, query):
    os.environ["OPENAI_API_KEY"] = "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"  # personal key

    # Load the document
    loader = TextLoader(path)
    ifc_model = loader.load()

    # Split the document into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    texts = text_splitter.split_documents(ifc_model)
    embeddings = OpenAIEmbeddings()

    # Create a vectorstore from the documents
    docsearch = Chroma.from_documents(texts, embeddings)

    # Prompt template
    prompt_template = """Given the following ifc file that contains information about a building information model with filetype
                ifc and a question, create a final answer.

                Respond in German.
                
                Model name: {context}

                QUESTION: {question}
                =========
                FINAL ANSWER IN German:"""

    # Create a prompt using the template
    prompt = PromptTemplate(template=prompt_template, input_variables=["question", "context"])

    # Create context
    context = path.split("/")[-1].split(".")[0]

    # Prompt kwargs
    chain_type_kwargs = {"prompt": prompt}

    # Create a question-answering chain using the index
    llm = ChatOpenAI(model_name='gpt-3.5-turbo-16k')
    chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.as_retriever(), chain_type_kwargs=chain_type_kwargs)

    # Pass a query to the chain
    response = chain({"query": query})
    return response['result']


if __name__ == '__main__':
    path = "../data_ifc_models/Testmodell.ifc"
    query = "Welche IFC Version hat das Modell?"
    print("Mit welcher CAD Anwendung wurde das Modell erstellt?")
    print(startLanguageModel(path, "Mit welcher CAD Anwendung wurde das Modell erstellt?"))
