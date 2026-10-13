# CogniMesh Universal Markdown Formatting Guidelines (GFM)

## 1. Portable Formatting (Cross-Platform Compatibility)
- **No Complex LaTeX Math:** Avoid `$$` or `$` LaTeX notation, as standard viewers (Dev.to, Medium, Notion) do not render KaTeX natively. Express mathematical formulas, limits, and metrics using clean Unicode text inside code blocks or bullet points.
- **Universal Code Blocks:** Always wrap math, equations, ASCII flowcharts, or code inside standard fenced code blocks (e.g., ```text, ```java, ```python).

## 2. YAML Frontmatter & Headers
- **Frontmatter:** Begin with a clean YAML block:
  ---
  title: "Article Title"
  date: YYYY-MM-DD
  author: CogniMesh AI
  tags: [tag1, tag2, tag3]
  ---
- **Header Hierarchy:** Use `##` for main sections and `###` for sub-sections. Never use `#` inside the body.

## 3. Typography & Spacing
- **TL;DR:** Always include a `> **TL;DR:**` blockquote right after the frontmatter.
- **Short Paragraphs:** Limit paragraphs to a maximum of 3-4 lines for clean readability.
- **Bold Emphasis:** Use **bold** for key technical terms on first mention.
- **Inline Code:** Wrap class names, methods, parameters, and variable names in single backticks (e.g., `UserRepository`).

## 4. Diagram & ASCII Safety
- Keep ASCII diagrams compact (maximum 60 characters wide) to prevent horizontal scrolling or wrapping on mobile screens and narrow text editors.