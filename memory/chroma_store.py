import chromadb

client = chromadb.PersistentClient(

    path="./chroma_db"

)

collection = client.get_or_create_collection(

    name="research_memory"

)

def store_research(query, summary):

    collection.add(

        documents=[summary],

        metadatas=[{"query": query}],

        ids=[query]
    )

def retrieve_research(query):

    results = collection.query(

        query_texts=[query],

        n_results=2
    )

    return results