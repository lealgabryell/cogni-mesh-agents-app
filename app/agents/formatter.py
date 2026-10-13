import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from app.core.config import settings
from app.core.utils import content_to_text
from app.graph.state import AgentState

def load_formatting_guidelines() -> str:
    """Loads the external formatting guidelines document if it exists."""
    guidelines_path = os.path.join(os.getcwd(), "app", "knowledge", "formatting_guidelines.md")
    if os.path.exists(guidelines_path):
        with open(guidelines_path, "r", encoding="utf-8") as file:
            return file.read()
    return ""

def formatter_node(state: AgentState) -> AgentState:
    """
    Formatter Agent Node:
    Takes the approved draft and packages it for publishing.
    Enriched by external formatting guidelines from the knowledge base.
    """
    print(f"--- FORMATTER AGENT: Polishing final output for -> '{state['topic']}' ---")

    llm = ChatGoogleGenerativeAI(
        model=settings.DEFAULT_MODEL_NAME,
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=0.1
    )

    approved_draft = state.get("draft_content", "")
    
    # Load external context document
    formatting_guidelines = load_formatting_guidelines()

    # Base Persona
    system_prompt = (
        "You are an Expert Technical Publisher and Markdown Formatter. "
        "Your task is to take a finalized technical article and format it perfectly for a developer blog.\n\n"
        "REQUIREMENTS:\n"
        "1. DO NOT change the technical explanations, tone, or core content of the article.\n"
        "2. Add a YAML frontmatter block at the very top.\n"
        "3. Add a '> **TL;DR:**' blockquote right after the frontmatter with a 2-sentence executive summary.\n"
        "4. Output ONLY the final Markdown text."
    )

    # Inject External Context (Formatting Guidelines) if available
    if formatting_guidelines:
        system_prompt += (
            "\n\nEXTERNAL KNOWLEDGE - FORMATTING GUIDELINES:\n"
            "You MUST strictly adhere to these formatting rules and best practices:\n"
            f"{formatting_guidelines}\n"
        )

    user_content = (
        f"Original Topic: {state['topic']}\n\n"
        f"Approved Draft:\n{approved_draft}"
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_content)
    ]

    response = llm.invoke(messages)

    return {
        "final_output": content_to_text(response.content).strip()
    }