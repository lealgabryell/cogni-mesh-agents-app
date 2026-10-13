import os
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from app.core.config import settings
from app.graph.state import AgentState

# 1. Define the Structured Output Schema using Pydantic
class ReviewOutput(BaseModel):
    is_approved: bool = Field(
        description="Set to True if the article meets all quality standards and is ready for publishing. False otherwise."
    )
    feedback: str = Field(
        description="If rejected, provide specific, actionable feedback for the Writer to fix. If approved, leave empty."
    )

def load_review_strategies() -> str:
    """Loads the external review strategies document if it exists."""
    strategies_path = os.path.join(os.getcwd(), "app", "knowledge", "review_strategies.md")
    if os.path.exists(strategies_path):
        with open(strategies_path, "r", encoding="utf-8") as file:
            return file.read()
    return ""

def reviewer_node(state: AgentState) -> AgentState:
    """
    Reviewer Agent Node:
    Acts as a strict Tech Lead. Evaluates the draft against the original research
    and the strict review strategies from the knowledge base.
    """
    print(f"--- REVIEWER AGENT: Evaluating draft for -> '{state['topic']}' ---")

    llm = ChatGoogleGenerativeAI(
        model=settings.DEFAULT_MODEL_NAME,
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=0.1 
    )

    structured_llm = llm.with_structured_output(ReviewOutput)

    formatted_research = "\n".join(state.get("research_data", []))
    draft = state.get("draft_content", "")
    current_revisions = state.get("revision_count", 0)

    # Load external context document
    review_strategies = load_review_strategies()

    # Base Persona
    system_prompt = (
        "You are an unforgiving Principal Engineer and Technical Editor. "
        "Your job is to review a technical article draft against the raw research data.\n\n"
        "If the draft fails ANY criteria, set 'is_approved' to False and provide brutal, actionable 'feedback'.\n"
        "If it is excellent, set 'is_approved' to True."
    )

    # Inject External Context (Review Strategies) if available
    if review_strategies:
        system_prompt += (
            "\n\nEXTERNAL KNOWLEDGE - REVIEW STRATEGIES:\n"
            "You MUST evaluate the draft strictly based on these guidelines:\n"
            f"{review_strategies}\n"
        )

    user_content = (
        f"Topic: {state['topic']}\n\n"
        f"Raw Research Data:\n{formatted_research}\n\n"
        f"Article Draft to Review:\n{draft}"
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_content)
    ]

    result: ReviewOutput = structured_llm.invoke(messages)

    return {
        "is_approved": result.is_approved,
        "review_feedback": result.feedback,
        "revision_count": current_revisions + 1
    }