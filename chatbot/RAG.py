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
        description="The news source that published the article.",
        type="string",
    ),
    AttributeInfo(
        name="time",
        description="The Unix timestamp in milliseconds.",
        type="integer",
    )]
document_content_description = "A news article about some journalistic topic."

embedding_function = SentenceTransformerEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

vector_db = Chroma(
    persist_directory="../vector_db",
    embedding_function=embedding_function,
)

llm = ChatOpenAI(openai_api_key="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", temperature=0)
retriever = SelfQueryRetriever.from_llm(
    llm, vector_db, document_content_description, metadata_field_info, verbose=True,search_kwargs={'k': 4}, 
)

retrieved_docs = retriever.get_relevant_documents("Retrieve articles written by the publishing source \"The Associated Press\"")
for i in retrieved_docs:
    print(i.metadata)

temp_vector_store = Chroma.from_documents(retrieved_docs, embedding_function)
subtext_retriever = temp_vector_store.as_retriever()

template = """Answer the question based only on the following supplied articles:
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

result = chain.invoke("What are the publishing sources of the provided articles? Summarize the contents of each article please.")
print(result)