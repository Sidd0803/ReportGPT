from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chat_models import ChatOpenAI
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain.memory import ConversationBufferMemory
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.chains import ConversationalRetrievalChain

#from decouple import config

#document info
metadata_field_info = [
    AttributeInfo(
        name="source",
        description="The news source that published the article.",
        type="string",
    ),
    AttributeInfo(
        name="time",
        description="The Unix timestamp in milliseconds. Convert to date and time format to answer user queries.",
        type="integer",
    )]
document_content_description = "A news article about some journalistic topic."


print("llm, chroma, embedding function ...")
# create chat model
llm = ChatOpenAI(openai_api_key="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", temperature=0)

embedding_function = SentenceTransformerEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

vector_db = Chroma(
    persist_directory="../vector_db",
    embedding_function=embedding_function,
)



print("prompt, memory, QA chain ...")
# create prompt
QA_prompt = PromptTemplate(
    template="""Use the following news articles to answer the user question. If you don't know the answer, say so. Don't make up an answer.""
chat_history: {chat_history}
Context: {text}
Question: {question}
Answer:""",
    input_variables=["text", "question", "chat_history"]
)

# create memory
memory = ConversationBufferMemory(
    return_messages=True, memory_key="chat_history")

qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    memory=memory,
    retriever=vector_db.as_retriever(
        search_kwargs={'fetch_k': 4, 'k': 3}, search_type='mmr'),
    chain_type="refine",
)

# create retriever chain
# qa_chain = SelfQueryRetriever.from_llm(
#     llm=llm,
#     vectorstore=vector_db,
#     document_contents=document_content_description,
#     metadata_field_info=metadata_field_info,
#     verbose=True
# )

question= "How did Alexei Navalny die?"

def rag(question: str) -> str:
    # call QA chain
    response = qa_chain({"question": question})

    return response.get("answer")

####SELF-QUERY RETRIEVER####
retriever = SelfQueryRetriever.from_llm(
    llm,
    vector_db,
    document_content_description,
    metadata_field_info,
)

print(retriever.invoke("I want all the articles written by the New York Times."))

# print("answering question:")
# docs = vector_db.max_marginal_relevance_search(question, k=4)
# for doc in docs:
#     print(doc, "\n\n\n")
# print(rag(question))
