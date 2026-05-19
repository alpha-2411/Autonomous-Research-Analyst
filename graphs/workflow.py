from langgraph.graph import StateGraph, END
from state.state import ResearchState
from agents.planner import planner_node
from agents.search_agent import search_node
from agents.extraction_agent import extraction_node
from agents.ranking_agent import ranking_node
from agents.summarizer_agent import summarizer_node
from agents.reflection_agent import reflection_node
from agents.memory_agent import memory_node
from agents.finalizer_agent import finalizer_node
from agents.memory_check_agent import memory_check_node

workflow = StateGraph(ResearchState)

workflow.add_node("planner", planner_node)
workflow.add_node("search", search_node)
workflow.add_node("extract", extraction_node)
workflow.add_node("rank", ranking_node)
workflow.add_node("summarize", summarizer_node)
workflow.add_node("reflect", reflection_node)
workflow.add_node("memory", memory_node)
workflow.add_node("finalize", finalizer_node)
workflow.add_node("memory_check", memory_check_node)

workflow.set_entry_point("memory_check")

def route_start(state):
    if state.get("found_in_memory", False):
        return END
    return "planner"

workflow.add_conditional_edges(
    "memory_check",
    route_start,
    {
        "planner": "planner",
        END: END
    }
)

workflow.add_edge("planner", "search")
workflow.add_edge("search", "extract")
workflow.add_edge("extract", "rank")
workflow.add_edge("rank", "summarize")
workflow.add_edge("summarize", "memory")
workflow.add_edge("memory", "reflect")
workflow.add_edge("finalize", END)

def route_decision(state):
    if state["needs_more_research"]:
        return "search"
    return "finalize"

workflow.add_conditional_edges(
    "reflect",
    route_decision,
    {
        "search": "search",
        "finalize": "finalize"
    }
)

app = workflow.compile()
