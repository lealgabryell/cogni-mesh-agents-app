from langgraph.graph import StateGraph, START, END
from app.graph.state import AgentState
from app.agents.researcher import researcher_node
from app.agents.writer import writer_node
from app.agents.reviewer import reviewer_node
from app.agents.formatter import formatter_node

# Define the maximum number of revision loops to prevent infinite API calls
MAX_REVISIONS = 3

def review_router(state: AgentState) -> str:
    """
    Conditional Routing Logic:
    Decides the next node based on the Reviewer's feedback and the revision limit.
    """
    is_approved = state.get("is_approved", False)
    revisions = state.get("revision_count", 0)

    print(f"--- ROUTER: Approved? {is_approved} | Revisions: {revisions}/{MAX_REVISIONS} ---")

    if is_approved:
        # If the tech lead approves, send to publishing
        return "formatter"
    
    if revisions >= MAX_REVISIONS:
        # If we hit the loop limit, force it to format whatever we have to avoid infinite loops
        print("--- ROUTER: Max revisions reached. Forcing output. ---")
        return "formatter"
    
    # Otherwise, send it back to the writer for corrections
    print("--- 🔙 ROUTER: Needs revision. Sending back to Writer. ---")
    return "writer"

def build_graph():
    """
    Builds and compiles the finite state machine for the multi-agent system.
    """
    # 1. Initialize the Graph with our specific State schema
    workflow = StateGraph(AgentState)

    # 2. Add all agent nodes to the graph
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("writer", writer_node)
    workflow.add_node("reviewer", reviewer_node)
    workflow.add_node("formatter", formatter_node)

    # 3. Define the Flow (Edges)
    # Start -> Researcher
    workflow.add_edge(START, "researcher")
    
    # Researcher -> Writer
    workflow.add_edge("researcher", "writer")
    
    # Writer -> Reviewer
    workflow.add_edge("writer", "reviewer")
    
    # Reviewer -> [Decision Router] -> Writer OR Formatter
    workflow.add_conditional_edges(
        "reviewer", 
        review_router,
        {
            "writer": "writer",       # If router returns "writer", go to writer node
            "formatter": "formatter"  # If router returns "formatter", go to formatter node
        }
    )

    # Formatter -> End
    workflow.add_edge("formatter", END)

    # 4. Compile the graph into an executable application
    app = workflow.compile()
    
    return app

# Expose the compiled graph instance to be used by the API or CLI
cognimesh_app = build_graph()