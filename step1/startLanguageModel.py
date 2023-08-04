from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.chat_models import AzureChatOpenAI, ChatOpenAI
from langchain.document_loaders import CSVLoader, DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI, OpenAIChat
import os

from langchain.vectorstores import Chroma


def startLanguageModel(path, query):
    os.environ["OPENAI_API_KEY"] = "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"
    print(query)

    # Load the document
    loader = TextLoader(path)
    ifc_model = loader.load()

    # Split the document into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=39, chunk_overlap=0, separators=[" ", ",", "\n", ":"])

    texts = text_splitter.split_documents(ifc_model)
    embeddings = OpenAIEmbeddings()
    db = Chroma.from_documents(texts, embeddings, persist_directory="./data/data-01.db")

    # Create an index using the loaded documents
    docsearch = VectorstoreIndexCreator().from_loaders([loader])
    print("test")

    # Prompt template
    prompt_template = """Given the following ifc file that contains information about a building information model with filetype
                ifc and a question, create a final answer.

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
    context = "IFC-Modell: " + path.split("/")[-1].split(".")[0]

    # Create a question-answering chain using the index
    llm = ChatOpenAI(model_name='gpt-3.5-turbo')
    chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.vectorstore.as_retriever(), chain_type_kwargs=chain_type_kwargs)

    # Pass a query to the chain
    response = chain({"query": query, "context": context})
    return response['result']
