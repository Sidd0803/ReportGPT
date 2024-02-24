#from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
#from langchain_community.llms import GPT4All
from langchain.chat_models import ChatOpenAI
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain.memory import ConversationBufferMemory
#from decouple import config

print("llm, chroma, embedding function ...")
# create chat model
llm = ChatOpenAI(openai_api_key="KEY", temperature=0)
#llm = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
#model = GPT4All(model="./models/mistral-7b-openorca.Q4_0.gguf", n_threads=8)

embedding_function = SentenceTransformerEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

vector_db = Chroma(
    persist_directory="../myvecdb",
    embedding_function=embedding_function,
)

# vector_db = Chroma(
#     persist_directory="../vector_db",
#     collection_name="rich_dad_poor_dad",
#     embedding_function=embedding_function,
# )

print("prompt, memory, QA chain ...")
# create prompt
QA_prompt = PromptTemplate(
    template="""Use the following pieces of context to answer the user question.
chat_history: {chat_history}
Context: {text}
Question: {question}
Answer:""",
    input_variables=["text", "question", "chat_history"]
)

# create memory
memory = ConversationBufferMemory(
    return_messages=True, memory_key="chat_history")

# create retriever chain
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    memory=memory,
    retriever=vector_db.as_retriever(
        search_kwargs={'fetch_k': 4, 'k': 3}, search_type='mmr'),
    chain_type="refine",
)

# question
question = "What is the mission of Starlab?"


def rag(question: str) -> str:
    # call QA chain
    response = qa_chain({"question": question})

    return response.get("answer")

print("answering question:")
print(rag(question))