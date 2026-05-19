from memory.chroma_store import (
    store_research,
    retrieve_research
)

def memory_node(state):

    query = state["query"]

    summary = state["research_summary"]

    store_research(query, summary)

    memory_results = retrieve_research(query)

    return {

        "memory_results": str(memory_results)
    }