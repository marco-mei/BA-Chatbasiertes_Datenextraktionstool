import os
from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma


def get_chain(path):
    """Takes a path to an ifc file and returns a language model that can answer questions about the ifc file."""
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
                Answer detailed and in full sentences. Round all number to two decimal places.
                Below the short answer you should add a long answer that contains more information and reasons for your answer (Max. 2 sentences).

                Respond in German.
                
                Model name: {context}

                QUESTION: {question}
                =========
                FINAL ANSWER IN German:"""

    # Create a prompt using the template
    prompt = PromptTemplate(template=prompt_template, input_variables=["question", "context"])

    # Prompt kwargs
    chain_type_kwargs = {"prompt": prompt}

    # Configure the language model
    llm = ChatOpenAI(model_name='gpt-3.5-turbo-16k', temperature=0)

    # Create a question-answering chain using the index
    chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.as_retriever(), chain_type_kwargs=chain_type_kwargs)
    return chain


def generateAnswer(path, query, chain):
    """Takes a path to an ifc file, a query and a language model and returns an answer to the query."""

    # Create context
    context = path.split("/")[-1].split(".")[0]

    response = chain({"query": query, "context": context})
    return response['result']


if __name__ == '__main__':
    path = "../data_ifc_models/Beispielhaus.ifc"
    query = "Welche Fläche haben die Fenster?"
    chain = get_chain(path)
    print(f"{query}:")
    print(generateAnswer(path, query, chain))
