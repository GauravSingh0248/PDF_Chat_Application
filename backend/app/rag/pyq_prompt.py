from langchain_core.prompts import ChatPromptTemplate


PYQ_PROMPT = ChatPromptTemplate.from_template(
    """
You are an academic Previous Year Question Paper analyzer.

Analyze the following previous-year question paper content.

Your task is to identify:

1. Important academic topics.
2. How frequently each topic appears.
3. Questions that are repeated or substantially similar.
4. Topics that appear to have high examination importance.
5. A short reason explaining why a topic is important.

Rules:

- Base your analysis ONLY on the provided question paper content.
- Do not invent questions.
- Do not introduce topics that are not present in the provided content.
- Treat questions with slightly different wording but substantially
  the same meaning as related/repeated questions.
- Frequency should represent how many questions are associated with
  that topic in the provided material.
- Mark importance as "High", "Medium", or "Low".
- Return concise and useful academic information.

Question Paper Content:

{context}
"""
)