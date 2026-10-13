def content_to_text(content: str | list) -> str:
    """Normalizes LangChain message content (str or list of blocks) to plain text."""
    if isinstance(content, str):
        return content

    text_parts = []
    for block in content:
        if isinstance(block, str):
            text_parts.append(block)
        elif isinstance(block, dict) and isinstance(block.get("text"), str):
            text_parts.append(block["text"])

    return "\n".join(text_parts)
