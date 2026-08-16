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