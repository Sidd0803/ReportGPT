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
        name="title",
        description="The title of the news article. If no title was available, the string will just say \"no title provided\".",
        type="string",
    ),
    AttributeInfo(
        name="description",
        description="A brief description of the news article. If no description was available, the string will just say \"no description provided\".",
        type="string"
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



print("memory, QA chain ...")

# create memory
memory = ConversationBufferMemory(
    return_messages=True, memory_key="chat_history")

qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    memory=memory,
    retriever=vector_db.as_retriever(
        search_kwargs={'k': 10}, search_type='mmr'),
    chain_type="refine",
)

question= "What has President Zelensky's policy lately been like?"

def rag(question: str) -> str:
    # call QA chain
    response = qa_chain({"question": question})

    return response.get("answer")

print("answering question:")
print(rag(question))
