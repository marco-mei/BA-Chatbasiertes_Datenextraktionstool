from langchain import PromptTemplate
from langchain.chains import RetrievalQA, RetrievalQAWithSourcesChain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.document_loaders import TextLoader, DirectoryLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma

embeddings = OpenAIEmbeddings()
data = './data/data-01.db'


def load_data():
    loader = DirectoryLoader('./data/', glob='**/*.txt', loader_cls=TextLoader)
    loader.loader_kwargs['encoding'] = 'utf-8'
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=39, chunk_overlap=0, separators=[" ", ",", "\n", ":"])

    texts = text_splitter.split_documents(documents)
    db = Chroma.from_documents(texts, embeddings, persist_directory=data)
    print(loader)


load_data()

db = Chroma(persist_directory=data, embedding_function=embeddings)

retriever = db.as_retriever(search_type="mmr")

template = """Given the following txt file that contains information about a building information model in with filetype 
ifc and a question, create a final answer. Every row in the file describes a building element and consists each of 
multiple key-value pairs. The key is separated from the value by a colon. The key is always a string and the value
can be a string or a number. The key-value pairs are separated by a comma. The file is encoded in UTF-8.
If you don't know the answer, just say that you don't know. Don't try to make up an answer.
Respond in German.

QUESTION: {question}
=========
{summaries}
=========
FINAL ANSWER IN German:"""
PROMPT = PromptTemplate(template=template, input_variables=["summaries", "question"])

chain = load_qa_with_sources_chain(OpenAI(temperature=0), chain_type="stuff", prompt=PROMPT)


while True:
    question = input("Question: ")
    documents = []

    answer = chain({"input_documents": retriever.get_relevant_documents(question), "question": question}, return_only_outputs=False)

    input_documents = answer['input_documents']
    for document in input_documents:
        documents.append(document.__dict__['metadata']['source'])

    documents = list(set(documents))

    print("Documents: ", documents)

    print("Answer: ", answer['output_text'])
    print("")
