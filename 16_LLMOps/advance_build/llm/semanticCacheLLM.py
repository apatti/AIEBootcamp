from langchain_core.runnables import Runnable
from langchain_core.documents import Document
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
import hashlib
from langchain_community.storage import SQLStore
from langchain_qdrant import QdrantVectorStore
from langchain.embeddings import CacheBackedEmbeddings

class SemanticCacheLLM(Runnable):
    def __init__(self,collection_name, hf_embeddings,llm):
        client = QdrantClient(":memory:")
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
        )
        # Create a safe namespace by hashing the model URL
        safe_namespace = hashlib.md5(hf_embeddings.model.encode()).hexdigest()
        
        sql_query_store = SQLStore(namespace=safe_namespace, db_url="sqlite:///db/query_embeddings_app_cache.db")
        sql_query_store.create_schema()
        
        
        cached_embedder = CacheBackedEmbeddings.from_bytes_store(
            hf_embeddings, sql_query_store, namespace=safe_namespace, batch_size=32,query_embedding_cache=True
        )
        
        # Typical QDrant Vector Store Set-up
        queryVectorstore = QdrantVectorStore(
            client=client,
            collection_name=collection_name,
            embedding=cached_embedder)

        self.__store = queryVectorstore
        self.__retriever = queryVectorstore.as_retriever(search_kwargs={"k": 1})
        self.llm = llm

    def invoke(
        self,
        inputs,
        run_manager= None,
    ):
        prompt = inputs["question"]
        print(f"Prompt: {prompt}")
        cache_prompt = self.__retriever.invoke(prompt)
        if cache_prompt:
            return {"response":cache_prompt[0].metadata['response']}

        response = self.llm.invoke(inputs["chat_prompt"])
        doc = Document(page_content=prompt,metadata={'response':response})
        self.__store.add_documents([doc])
        return response