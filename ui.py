import streamlit as st
from graphs.workflow import app as workflow_app

st.set_page_config(
    page_title="Autonomous Research Analyst",
    page_icon="🔎",
    layout="wide"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>
    .reportview-container {
        background: #fafafa;
    }

    .metric-card {
        background-color: white;
        border-radius: 10px;
        padding: 18px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.08);
        text-align: center;
        margin-bottom: 20px;
    }

    .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: #1f77b4;
    }

    .metric-label {
        font-size: 14px;
        color: #555;
    }

    .status-running {
        color: orange;
        font-weight: bold;
    }

    .status-success {
        color: green;
        font-weight: bold;
    }

    .status-failed {
        color: red;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.title("🔎 Autonomous Research Analyst")

st.markdown("""
### AI-powered multi-agent research and analysis system

This autonomous platform performs:

- Research Planning
- Internet Retrieval
- Concurrent Extraction
- Source Ranking
- Research Summarization
- Reflection & Self-Critique
- Persistent Vector Memory
""")

st.divider()

# -----------------------------
# Input
# -----------------------------
query = st.text_input(
    "Enter Research Query",
    placeholder="e.g., Impact of Quantum Computing on Cryptography"
)

# -----------------------------
# Run Button
# -----------------------------
if st.button("Run Research", type="primary"):

    if not query.strip():

        st.warning("Please enter a research query.")

    else:

        st.markdown("## ⚙️ Live Pipeline Execution")

        # -----------------------------
        # Progress UI
        # -----------------------------
        status_text = st.empty()

        progress_bar = st.progress(0)

        # -----------------------------
        # Metrics Dashboard
        # -----------------------------
        col1, col2, col3 = st.columns(3)

        metric_iterations = col1.empty()

        metric_sources = col2.empty()

        metric_status = col3.empty()

        def update_metrics(iteration=0, sources=0, status="Running"):

            metric_iterations.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-value">{iteration}</div>
                    <div class="metric-label">Research Cycles</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            metric_sources.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-value">{sources}</div>
                    <div class="metric-label">Sources Extracted</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            metric_status.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-value">{status}</div>
                    <div class="metric-label">Pipeline Status</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        update_metrics(status="Initializing")

        # -----------------------------
        # Live Logs
        # -----------------------------
        with st.expander("🧠 Live Agent Logs", expanded=True):

            log_container = st.empty()

            logs = ""

        # -----------------------------
        # Initial Graph State
        # -----------------------------
        inputs = {

            "query": query,

            "iteration_count": 0,

            "search_results": [],

            "extracted_content": [],

            "source_rankings": ""
        }

        # -----------------------------
        # IMPORTANT FIX
        # Proper state aggregation
        # -----------------------------
        final_state = {}

        current_sources = 0

        current_iteration = 0

        step = 0

        estimated_steps = 10

        # -----------------------------
        # Stream Execution
        # -----------------------------
        try:

            for output in workflow_app.stream(inputs):

                for node_name, state_update in output.items():

                    # -----------------------------
                    # CRITICAL FIX
                    # Aggregate ALL states
                    # -----------------------------
                    for key, value in state_update.items():
                        if key in ["search_results", "extracted_content"]:
                            if key not in final_state:
                                final_state[key] = []
                            final_state[key].extend(value)
                        else:
                            final_state[key] = value

                    step += 1

                    progress = min(step / estimated_steps, 1.0)

                    progress_bar.progress(progress)

                    # -----------------------------
                    # Logging
                    # -----------------------------
                    status_msg = f"Agent '{node_name}' completed."

                    logs += f"✅ {status_msg}\n\n"

                    log_container.markdown(logs)

                    status_text.markdown(
                        f"### Current Action: `{status_msg}`"
                    )

                    # -----------------------------
                    # Metrics Updates
                    # -----------------------------
                    if "extracted_content" in final_state:

                        current_sources = len(
                            final_state["extracted_content"]
                        )

                    if "iteration_count" in final_state:

                        current_iteration = final_state[
                            "iteration_count"
                        ]

                    update_metrics(

                        iteration=current_iteration,

                        sources=current_sources,

                        status=f"Running ({node_name})"
                    )

            # -----------------------------
            # Pipeline Complete
            # -----------------------------
            progress_bar.progress(1.0)

            update_metrics(

                iteration=current_iteration,

                sources=current_sources,

                status="Completed 🎉"
            )

            status_text.success(
                "Research pipeline completed successfully!"
            )

            # Save the final report
            from tools.report_saver import save_report
            if "research_summary" in final_state:
                saved_file = save_report(query, final_state["research_summary"])
                final_state["saved_report"] = saved_file

            st.divider()

            # -----------------------------
            # Final Report
            # -----------------------------
            st.header("📋 Final Research Report")

            tabs = st.tabs([
                "Summary",
                "Source Rankings",
                "Research Plan",
                "Reflection"
            ])

            # -----------------------------
            # Summary Tab
            # -----------------------------
            with tabs[0]:

                st.subheader("Comprehensive Summary")

                summary = final_state.get(

                    "research_summary",

                    "No summary generated."
                )

                st.write(summary)

                saved_report = final_state.get("saved_report")

                if saved_report:

                    st.success(
                        f"💾 Report saved locally at: {saved_report}"
                    )

            # -----------------------------
            # Source Rankings
            # -----------------------------
            with tabs[1]:

                st.subheader(
                    "Credibility & Relevance Rankings"
                )

                rankings = final_state.get(

                    "source_rankings",

                    ""
                )

                if rankings:

                    st.markdown(rankings)

                else:

                    st.info("No rankings available.")

            # -----------------------------
            # Planner Output
            # -----------------------------
            with tabs[2]:

                st.subheader("Original Research Plan")

                planner_output = final_state.get(

                    "planner_output",

                    "No plan available."
                )

                st.write(planner_output)

            # -----------------------------
            # Reflection Output
            # -----------------------------
            with tabs[3]:

                st.subheader("Final Reflection")

                reflection = final_state.get(

                    "reflection",

                    "No reflection available."
                )

                st.write(reflection)

        # -----------------------------
        # Exception Handling
        # -----------------------------
        except Exception as e:

            progress_bar.progress(1.0)

            update_metrics(status="Failed ❌")

            st.error(f"An error occurred:\n\n{e}")