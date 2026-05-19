from memory.chroma_store import retrieve_research
from loguru import logger

def memory_check_node(state):
    query = state["query"]
    logger.info(f"Memory Check Agent: Searching Chroma DB for '{query}'")
    
    results = retrieve_research(query)
    
    # Chroma returns lists of lists for documents and distances
    if results and "documents" in results and results["documents"] and len(results["documents"][0]) > 0:
        distances = results.get("distances", [[1.0]])[0]
        # Distance < 0.3 typically means very high similarity in default Chroma embeddings
        if distances and len(distances) > 0 and distances[0] < 0.3:
            logger.info("Memory Check Agent: Found highly relevant past research!")
            return {
                "research_summary": results["documents"][0][0],
                "found_in_memory": True,
                "planner_output": "Research retrieved from memory (Chroma DB). Skipped planning phase.",
                "source_rankings": "Archived memory - sources were validated during the original research.",
                "reflection": "Research retrieved directly from memory. No further reflection needed."
            }
            
    logger.info("Memory Check Agent: No relevant research found. Starting fresh.")
    return {"found_in_memory": False}
