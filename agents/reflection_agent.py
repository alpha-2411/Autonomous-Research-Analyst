from config.llm_config import get_llm
from prompts.research_prompts import REFLECTION_PROMPT
from loguru import logger

def reflection_node(state):
    summary = state["research_summary"]
    current_iteration = state.get("iteration_count", 0)
    
    logger.info(f"Reflection Agent: Evaluating summary (Iteration {current_iteration})")
    
    llm = get_llm()
    prompt = REFLECTION_PROMPT.format(summary=summary)
    
    response = llm.invoke(prompt)
    reflection_text = response.content
    
    needs_more_research = (
        "YES" in reflection_text.upper() and current_iteration < 2
    )
    
    if needs_more_research:
        logger.info("Reflection Agent: More research is needed. Triggering next iteration.")
    else:
        logger.info("Reflection Agent: Research is comprehensive or max iterations reached.")
        
    return {
        "reflection": reflection_text,
        "needs_more_research": needs_more_research,
        "iteration_count": current_iteration + 1
    }