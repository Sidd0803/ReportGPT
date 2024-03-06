from langchain_community.vectorstores import Chroma
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain.chains.query_constructor.base import AttributeInfo
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

metadata_field_info = [
    AttributeInfo(
        name="source",
        description="A string of the news source that published the article.",
        type="string",
    ),
    AttributeInfo(
        name="title",
        description="The title of the news article.",
        type="string",
    ),
    AttributeInfo(
        name="description",
        description="A brief description of the news article. If no description was available, the string will just say \"no description provided\".",
        type="string"
    )]
document_content_description = "A snippet from a news article about some journalistic topic."

embedding_function = SentenceTransformerEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

vector_db = Chroma(
    # persist_directory="../vector_dbV2wChunking",
    persist_directory="../vector_db",
    embedding_function=embedding_function,
)

llm = ChatOpenAI(openai_api_key="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", temperature=0)
retriever = SelfQueryRetriever.from_llm(
    llm, vector_db, document_content_description, metadata_field_info, verbose=True,search_kwargs={'k': 10},search_type='mmr'
)

print("trying to retrieve articles")
#retrieved_docs = retriever.get_relevant_documents("Retrieve documents with titles that contain the string \"How the Kremlin weaponized Russian history\"")
retrieved_docs = retriever.get_relevant_documents("Retrieve articles by the source \"The New York Times\".")
for i in retrieved_docs:
    print(i.metadata)
print([len(retrieved_doc.page_content) for retrieved_doc in retrieved_docs])

temp_vector_store = Chroma.from_documents(retrieved_docs, embedding_function)
subtext_retriever = temp_vector_store.as_retriever()

template = """You are given a specific newsroom's coverage of the Ukraine-Russia War. Answer the question based only on the following context:
{context}
Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

chain = (
    {"context": subtext_retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

result = chain.invoke("With what tone does the New York Times write about Zelensky?")
print(result)

def rag(question: str) -> str:
    return chain.invoke(question)

  