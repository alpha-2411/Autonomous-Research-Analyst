from config.llm_config import get_llm
from prompts.research_prompts import PLANNER_PROMPT
from loguru import logger

def planner_node(state):
    query = state["query"]
    logger.info(f"Planner Agent: Generating research plan for '{query}'")
    
    llm = get_llm()
    prompt = PLANNER_PROMPT.format(query=query)
    
    response = llm.invoke(prompt)
    
    return {
        "planner_output": response.content
    }