from typing import List, TypedDict


class AgentState(TypedDict):
    """
    Represents the state passed between agents in the CogniMesh graph.
    """
    topic: str                  # The original topic provided by the user
    research_data: List[str]    # Raw data and references gathered by the Researcher
    draft_content: str          # Current version of the article drafted by the Writer
    review_feedback: str        # Critical feedback provided by the Reviewer
    revision_count: int         # To track and limit revision loops
    is_approved: bool           # Flag indicating if the Reviewer approved the draft
    final_output: str           # Final formatted Markdown output