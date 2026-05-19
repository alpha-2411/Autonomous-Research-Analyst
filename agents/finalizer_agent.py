from tools.report_saver import save_report

def finalizer_node(state):

    query = state["query"]

    summary = state["research_summary"]

    saved_file = save_report(query, summary)

    return {

        "saved_report": saved_file
    }