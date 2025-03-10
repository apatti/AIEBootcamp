import time
# Function to time embedding generation
def time_embedding(text, embedder):
    start_time = time.time()
    embedder.embed_query(text)  # Embed the text
    end_time = time.time()
    return end_time - start_time

def time_retrieval(prompt, retriever):
    start_time = time.time()
    retriever.invoke(prompt)
    end_time = time.time()
    return end_time - start_time

