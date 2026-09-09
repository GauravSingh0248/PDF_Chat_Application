from langchain_core.prompts import ChatPromptTemplate

PYQ_PROMPT = ChatPromptTemplate.from_template(
    """
    You are an academic Previous Year Question (PYQ) paper analyzer.

    The user has uploaded MULTIPLE previous-year question papers for the same
    subject (different years). Analyze them TOGETHER as a cross-year set.

    {subject_line}

    Your goals:
    1. Find topics that appear across years and rank them by importance.
    2. Find questions that are repeated (same or nearly identical) across years.
    3. Find questions that are similar in meaning even if wording differs.
    4. Identify the most important topics for exam preparation.
    5. Write a short exam-focus summary based on patterns across years.

    Rules:
    - Use ONLY the provided question-paper content.
    - Do not invent questions or topics that are not supported by the papers.
    - Treat slightly different wording with the same meaning as the SAME question family.
    - Frequency must count how many papers / occurrences support the item.
    - For repeated_questions, frequency must be at least 2.
    - For similar_questions, group variants that test the same concept.
    - years_appeared must use the paper labels provided in the content headers
      (filename / year label).
    - Mark topic importance as exactly one of: High, Medium, Low.
    - Prefer High importance for topics that appear in many years or repeatedly.
    - Sort topics and repeated/similar groups by frequency descending when possible.
    - Be concise and useful for a student preparing for an upcoming exam.

    OUTPUT FORMAT:
    Return ONLY valid JSON. No markdown. No code fences.
    Use EXACTLY these field names (do not rename them):

    {{
      "subject": "string or null",
      "papers_analyzed": ["filename1.pdf", "filename2.pdf"],
      "topics": [
        {{
          "topic": "string",
          "frequency": 2,
          "years_appeared": ["label1", "label2"],
          "importance": "High",
          "reason": "short explanation"
        }}
      ],
      "repeated_questions": [
        {{
          "question": "canonical question text",
          "frequency": 2,
          "years_appeared": ["label1", "label2"],
          "topic": "string"
        }}
      ],
      "similar_questions": [
        {{
          "representative_question": "main question text",
          "similar_variants": ["variant A", "variant B"],
          "frequency": 2,
          "years_appeared": ["label1", "label2"],
          "topic": "string"
        }}
      ],
      "important_topics": ["topic1", "topic2"],
      "exam_focus_summary": "short summary string"
    }}

    Field name requirements:
    - topics[].reason is REQUIRED (never omit it)
    - repeated_questions[].question (NOT question_family)
    - similar_questions[].representative_question (NOT group)
    - similar_questions[].similar_variants must be a list of strings
    - importance must be exactly High, Medium, or Low

    Multi-year question paper content:

    {context}
    """
)
