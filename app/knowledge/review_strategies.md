# CogniMesh Technical Review Strategies & Evaluation Matrix

## 1. Hallucination & Fact-Checking (Critical)
- **Strict Adherence:** The draft MUST NOT introduce external concepts, frameworks, statistics, or metrics that are absent from the provided Research Data.
- **Precision Verification:** If the research states a technology "improves latency", reject the draft if it hallucinates numbers like "improves latency by 90%".

## 2. Structural & Markdown Integrity
- **Fluff Detection:** Instantly reject drafts containing generic introductions (e.g., "In the ever-evolving world of technology...") or conversational conclusions.
- **Formatting Rules:** Ensure all architectural patterns, classes, and technical terms are properly formatted with `inline code` backticks. 
- **Density:** The text must be highly dense and objective. Reject paragraphs that use 4 sentences to explain what could be said in 1.

## 3. Feedback Generation Protocol
When setting `is_approved` to False, your `feedback` MUST follow these rules:
- **Be Specific and Actionable:** Do NOT say "Fix the tone." DO say "Remove the marketing language in section X and replace it with objective engineering facts."
- **Locate the Error:** Always quote or reference the exact section or paragraph that needs rewriting.
- **Do Not Rewrite:** Give instructions on *how* to fix it, do not write the fixed text yourself.