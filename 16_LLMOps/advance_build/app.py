import os
import chainlit as cl
from dotenv import load_dotenv
import uuid
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader

from operator import itemgetter
from langchain_community.document_loaders import TextLoader
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.runnable.config import RunnableConfig
from tqdm.asyncio import tqdm_asyncio
import asyncio
from tqdm.asyncio import tqdm
import hashlib

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore
from langchain.embeddings import CacheBackedEmbeddings
from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings

from langchain_core.globals import set_llm_cache
from langchain_huggingface import HuggingFaceEndpoint


from operator import itemgetter
from langchain_core.runnables.passthrough import RunnablePassthrough

from langchain_community.storage import SQLStore
from llm.semanticCacheLLM import SemanticCacheLLM
from util.RAGTemplates import GetChatPrompt

import time
from langsmith import Client

lclient = Client()

load_dotenv()

HF_LLM_ENDPOINT = os.environ["HF_LLM_ENDPOINT"]
HF_EMBED_ENDPOINT = os.environ["HF_EMBED_ENDPOINT"]
HF_TOKEN = os.environ["HF_TOKEN"]

os.environ["LANGCHAIN_PROJECT"] = f"AIM Session 16 Advanced App - {uuid.uuid4().hex[0:8]}"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = os.environ["LANGCHAIN_API_KEY"]
os.environ["LANGCHAIN_TRACING_V2"] = "true"

print(os.environ["LANGCHAIN_API_KEY"])
print(os.environ["LANGCHAIN_PROJECT"])

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
Loader = PyMuPDFLoader
loader = Loader("DeepSeek_R1.pdf")
documents = loader.load()
docs = text_splitter.split_documents(documents)
for i, doc in enumerate(docs):
    doc.metadata["source"] = f"source_{i}"

hf_embeddings = HuggingFaceEndpointEmbeddings(
    model=HF_EMBED_ENDPOINT,
    task="feature-extraction",
)

def getRetriever(hf_embeddings,docs):
    collection_name = f"pdf_to_parse_{uuid.uuid4()}"
    client = QdrantClient(":memory:")
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=768, distance=Distance.COSINE),
    )

    # Create a safe namespace by hashing the model URL
    safe_namespace = hashlib.md5(hf_embeddings.model.encode()).hexdigest()

    sql_store = SQLStore(namespace=safe_namespace, db_url="sqlite:///db/embeddings_app_cache.db")
    sql_store.create_schema()

    cached_embedder = CacheBackedEmbeddings.from_bytes_store(
        hf_embeddings, sql_store, namespace=safe_namespace, batch_size=32
    )

    # Typical QDrant Vector Store Set-up
    vectorstore = QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=cached_embedder)
    vectorstore.add_documents(docs)

    return vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 1})

hf_llm = HuggingFaceEndpoint(
    endpoint_url=f"{HF_LLM_ENDPOINT}",
    task="text-generation",
    max_new_tokens=128,
    top_k=10,
    top_p=0.95,
    typical_p=0.95,
    temperature=0.01,
    repetition_penalty=1.03,
)

print("Setting up cache")
scLLM = SemanticCacheLLM("HW16-AdvancedBuild",hf_embeddings,hf_llm)
set_llm_cache(None)

@cl.on_chat_start
async def on_chat_start():
    retriever = getRetriever(hf_embeddings,docs)
    chat_prompt = GetChatPrompt()
    rag_cache_chain = (
        {"context": itemgetter("question") | retriever, "question": itemgetter("question")}
        | RunnablePassthrough.assign(context=itemgetter("context"))
        | {"chat_prompt":chat_prompt,"question":itemgetter("question")} | scLLM
    )
    print("Setting rag")
    cl.user_session.set("rag_cache_chain", rag_cache_chain)

@cl.on_message
async def on_message(message: cl.Message):
    rag_cache_chain = cl.user_session.get("rag_cache_chain")

    msg = cl.Message(content="")
    start_time = time.time()
    print(message.content)
    response = rag_cache_chain.invoke({"question": message.content})
    print(response)
    if isinstance(response, dict):
        response = response["response"]

    msg.content = response
    await msg.send()
    msg = cl.Message(content="")
    end_time = time.time()
    msg.content = f"Time taken: {end_time - start_time}"
    await msg.send()