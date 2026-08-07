class PromptBuilder:
    """
    Builds prompts for Enterprise AI RAG pipeline.
    """

    # ======================================================
    # Generic Prompt
    # ======================================================

    @staticmethod
    def build_prompt(context: str, question: str) -> str:

        prompt = f"""
You are an Enterprise AI Knowledge Assistant.

Answer ONLY using the context provided below.

If the answer is not available in the context, reply exactly:

"I could not find this information."

-------------------------
Context
-------------------------

{context}

-------------------------
Question
-------------------------

{question}

-------------------------
Answer
-------------------------
"""

        return prompt.strip()

    # ======================================================
    # Summary Prompt
    # ======================================================

    @staticmethod
    def build_summary_prompt(context: str) -> str:

        prompt = f"""
You are an expert document summarizer.

Summarize the following document into concise bullet points.

Document:

{context}

Summary:
"""

        return prompt.strip()

    # ======================================================
    # Question Answer Prompt
    # ======================================================

    @staticmethod
    def build_qa_prompt(
        context: str,
        question: str
    ) -> str:

        prompt = f"""
You are an Enterprise AI Knowledge Assistant.

Use ONLY the information provided below.

Context:

{context}

Question:

{question}

Answer:
"""

        return prompt.strip()