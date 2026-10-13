from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from app.core.config import settings
from app.core.utils import content_to_text
from app.graph.state import AgentState


def researcher_node(state: AgentState) -> AgentState:
    """
    Researcher Agent Node:
    Takes the user topic from the state, analyzes it, and gathers 
    structured technical research data.
    """
    print(f"--- RESEARCHER AGENT: Analyzing topic -> '{state['topic']}' ---")

    # Initialize the Google Gemini model via LangChain
    llm = ChatGoogleGenerativeAI(
        model=settings.DEFAULT_MODEL_NAME,
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=0.2  # Low temperature for more objective and factual technical research
    )

    # Define the specialized persona and instructions for the agent
    system_prompt = (
        "You are an Elite Technical Researcher and Principal Systems Architect. "
        "Your objective is to dissect the provided technical topic and extract deep, actionable engineering insights.\n\n"
        "CONSTRAINTS:\n"
        "- Strictly avoid marketing fluff, generic introductions, or conversational filler.\n"
        "- Focus entirely on technical depth, architectural trade-offs, and industry best practices.\n"
        "- Base your analysis on modern software engineering standards.\n\n"
        "OUTPUT FORMAT:\n"
        "Structure your research into a concise, data-driven markdown list covering these exact areas:\n"
        "1. Core Concepts & Mechanisms: How it works under the hood.\n"
        "2. Architectural Trade-offs: Pros, cons, and common bottlenecks.\n"
        "3. Use Cases & Anti-patterns: When to use it and when to avoid it.\n"
        "4. Modern Tooling & Ecosystem: Current industry standards related to the topic.\n\n"
        "Deliver ONLY the structured bullet points. Be precise and rigorous."
    )

    # Prepare messages for the LLM
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Research the following technical topic: {state['topic']}")
    ]

    # Invoke the model
    response = llm.invoke(messages)

    # Normalize LangChain's string or block-based content before storing research lines.
    response_text = content_to_text(response.content)
    research_bullets = [point.strip() for point in response_text.splitlines() if point.strip()]

    # Update the state (returning the fields we want to modify/add)
    return {
        "research_data": research_bullets
    }