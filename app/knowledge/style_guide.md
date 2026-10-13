# CogniMesh Technical Writing Style Guide

## 1. Voice and Tone
- **Authoritative but Accessible:** Write as a Senior Staff Engineer mentoring a mid-level developer.
- **Active Voice:** Always use active voice. (e.g., "The API returns a JSON" instead of "A JSON is returned by the API").
- **Clarity Over Complexity:** Avoid convoluted jargon when a simple term suffices.

## 2. Structural Patterns
- **TL;DR First:** If the section is long, start with a 1-sentence summary blockquote.
- **Progressive Disclosure:** Start with the high-level concept before diving into the code or raw data.
- **Transitions:** Avoid filler transitions like "Moving on to the next point". Use strong H2/H3 headings instead.

## 3. Formatting Rules
- **Code Entities:** Always wrap class names, variables, and file names in backticks (e.g., `UserService`, `app/core/config.py`).
- **Lists:** Prefer bulleted lists for items of equal importance, and numbered lists ONLY for sequential steps.
- **Warning/Notes:** Use blockquotes for critical architectural warnings (e.g., `> **Warning:** This approach increases database load.`)