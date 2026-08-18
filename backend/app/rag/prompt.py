from langchain_core.prompts import ChatPromptTemplate


RAG_PROMPT = ChatPromptTemplate.from_template(
    """
        You are a helpful assistant that answers questions based only on
        the provided document context.

        Rules:
        - Use only the information provided in the context.
        - If the answer cannot be found in the context, say:
        "I don't know based on the provided document."
        - Do not make up information.
        - Keep the answer clear and concise.

        Context:
        {context}

        Question:
        {question}

        Answer:
        """
)






QUIZ_PROMPT = ChatPromptTemplate.from_template(
    """
    You are an expert quiz generator.

    Generate exactly {number_of_questions} multiple-choice questions
    based ONLY on the provided document context.

    Rules:
    1. Every question must be answerable from the provided context.
    2. Each question must have exactly 4 options.
    3. Only one option must be correct.
    4. Do not use information outside the provided context.
    5. Do not create duplicate or very similar questions.
    6. Try to cover different parts of the provided context.
    7. Provide a clear explanation for the correct answer.

    Document Context:
    {context}
"""
)