import operator
from typing import TypedDict, List, Annotated

class ResearchState(TypedDict):

    query: str

    planner_output: str

    search_results: Annotated[List[dict], operator.add]

    extracted_content: Annotated[List[dict], operator.add]

    source_rankings: str

    research_summary: str

    reflection: str

    needs_more_research: bool

    iteration_count: int

    memory_results: str

    saved_report: str

    found_in_memory: bool
