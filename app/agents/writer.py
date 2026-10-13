import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from app.core.config import settings
from app.core.utils import content_to_text
from app.graph.state import AgentState

def load_style_guide() -> str:
    """Loads the external style guide document if it exists."""
    guide_path = os.path.join(os.getcwd(), "app", "knowledge", "style_guide.md")
    if os.path.exists(guide_path):
        with open(guide_path, "r", encoding="utf-8") as file:
            return file.read()
    return ""

def writer_node(state: AgentState) -> AgentState:
    """
    Technical Writer Agent Node:
    Synthesizes the raw research data into a high-quality article,
    enriched by external context (Style Guides) and strict instructions.
    """
    print(f"--- WRITER AGENT: Drafting article for -> '{state['topic']}' ---")

    llm = ChatGoogleGenerativeAI(
        model=settings.DEFAULT_MODEL_NAME,
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=0.3
    )

    formatted_research = "\n".join(state.get("research_data", []))
    feedback = state.get("review_feedback", "")
    is_revision = bool(feedback)
    
    # Load external context document
    style_guide = load_style_guide()

    # Base Persona
    system_prompt = (
        "You are an Expert Technical Writer and Staff Software Engineer. "
        "Your goal is to transform raw research data into a production-ready technical article.\n\n"
        "CONSTRAINTS:\n"
        "- NO fluff, NO marketing speak, NO generic introductions.\n"
        "- End the article abruptly after the last technical point.\n"
        "- Base your writing SOLELY on the provided research data.\n"
    )
    
    # Inject External Context (Style Guide) if available
    if style_guide:
        system_prompt += (
            "\nEXTERNAL KNOWLEDGE - STYLE GUIDE:\n"
            "You MUST strictly adhere to the following writing guidelines:\n"
            f"{style_guide}\n"
        )

    # Inject Revision Context
    if is_revision:
        system_prompt += (
            "\nCRITICAL REVISION INSTRUCTION:\n"
            "This is a REVISION. Your previous draft was rejected by the Reviewer.\n"
            "You MUST address the following feedback:\n"
            f"Reviewer Feedback: {feedback}\n"
        )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Topic: {state['topic']}\n\nResearch Data:\n{formatted_research}")
    ]

    response = llm.invoke(messages)
    
    return {
        "draft_content": content_to_text(response.content).strip()
    }