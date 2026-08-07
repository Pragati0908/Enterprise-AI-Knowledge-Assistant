"""
===============================================================
Enterprise AI Knowledge Assistant

RAG Service

Responsibilities
----------------
1. Retrieve relevant chunks from FAISS
2. Validate retrieval quality
3. Build prompts
4. Query the LLM
5. Return structured responses
6. Log the complete RAG pipeline
7. Support Streamlit Chat
8. Support Summarization
9. Support Generic Prompt Execution
===============================================================
"""

import logging
import time

from app.services.retriever import Retriever
from app.services.prompt_builder import PromptBuilder
from app.services.llm_service import LLMService


# ============================================================
# Logging Configuration
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# ============================================================
# Debug Configuration
# ============================================================

DEBUG = True


# ============================================================
# RAG Service
# ============================================================

class RAGService:
    """
    Complete Retrieval-Augmented Generation Service
    """

    FALLBACK_RESPONSE = "I could not find this information."

    DISTANCE_THRESHOLD = 1.35

    # ========================================================
    # Constructor
    # ========================================================

    def __init__(
        self,
        retriever: Retriever,
        prompt_builder: PromptBuilder,
        llm_service: LLMService
    ):

        self.retriever = retriever
        self.prompt_builder = prompt_builder
        self.llm_service = llm_service

    # ========================================================
    # Streamlit Chat Wrapper
    # ========================================================

    def chat(
        self,
        question: str,
        top_k: int = 3
    ) -> dict:
        """
        Wrapper used by the Streamlit chat interface.
        """

        logger.info("=" * 80)
        logger.info("STREAMLIT CHAT REQUEST")
        logger.info("=" * 80)

        start_time = time.time()

        result = self.ask(
            question=question,
            top_k=top_k
        )

        result["response_time"] = round(
            time.time() - start_time,
            2
        )

        logger.info(
            "Completed in %.2f seconds",
            result["response_time"]
        )

        return result

    # ========================================================
    # Ask Question
    # ========================================================

    def ask(
        self,
        question: str,
        top_k: int = 3
    ) -> dict:

        try:

            logger.info("=" * 80)
            logger.info("NEW QUESTION")
            logger.info(question)
            logger.info("=" * 80)

            # ------------------------------------------------
            # Retrieve Chunks
            # ------------------------------------------------

            logger.info(
                "Retrieving relevant document chunks..."
            )

            retrieved_chunks = self.retriever.retrieve(
                query=question,
                top_k=top_k
            )

            logger.info(
                "Retrieved %d chunks.",
                len(retrieved_chunks)
            )

            if len(retrieved_chunks) == 0:

                logger.warning(
                    "Retriever returned zero chunks."
                )

                return {
                    "success": True,
                    "question": question,
                    "answer": self.FALLBACK_RESPONSE,
                    "chunks_used": 0,
                    "sources": []
                }

            best_distance = retrieved_chunks[0]["distance"]

            logger.info(
                "Best FAISS distance : %.4f",
                best_distance
            )

            if best_distance > self.DISTANCE_THRESHOLD:

                logger.warning(
                    "Retrieval distance %.4f exceeds threshold %.2f",
                    best_distance,
                    self.DISTANCE_THRESHOLD
                )

                return {
                    "success": True,
                    "question": question,
                    "answer": self.FALLBACK_RESPONSE,
                    "chunks_used": 0,
                    "sources": []
                }

            # ------------------------------------------------
            # DEBUG : Show Retrieved Chunks
            # ------------------------------------------------

            if DEBUG:

                logger.info("=" * 80)
                logger.info("RETRIEVED CHUNKS")
                logger.info("=" * 80)

                for chunk in retrieved_chunks:

                    logger.info(
                        "Chunk ID : %s",
                        chunk["chunk_id"]
                    )

                    logger.info(
                        "Document : %s",
                        chunk["document"]
                    )

                    logger.info(
                        "Page : %s",
                        chunk["page"]
                    )

                    logger.info(
                        "Distance : %.4f",
                        chunk["distance"]
                    )

                    logger.info(
                        "Text Preview:\n%s",
                        chunk["text"][:250]
                    )

                    logger.info("-" * 80)

            # ------------------------------------------------
            # Build Context
            # ------------------------------------------------

            logger.info(
                "Building context from retrieved chunks..."
            )

            context = "\n\n".join(

                chunk["text"]

                for chunk in retrieved_chunks

            )

            logger.info(
                "Context length : %d characters",
                len(context)
            )

            # ------------------------------------------------
            # Build Prompt
            # ------------------------------------------------

            logger.info(
                "Building prompt..."
            )

            prompt = self.prompt_builder.build_prompt(
                context=context,
                question=question
            )

            if DEBUG:

                logger.info("=" * 80)
                logger.info("PROMPT SENT TO LLM")
                logger.info("=" * 80)
                logger.info(prompt)
                logger.info("=" * 80)

            # ------------------------------------------------
            # Generate Answer
            # ------------------------------------------------

            logger.info(
                "Sending prompt to LLM..."
            )

            answer = self.llm_service.generate(
                prompt
            )

            logger.info(
                "LLM response received."
            )

            if DEBUG:

                logger.info("=" * 80)
                logger.info("RAW LLM RESPONSE")
                logger.info("=" * 80)
                logger.info(answer)
                logger.info("=" * 80)

            answer = answer.strip()

            answer_lower = answer.lower()

            fallback_patterns = [

                "couldn't find",

                "could not find",

                "cannot find",

                "don't have enough information",

                "do not have enough information",

                "not enough information",

                "information is not available",

                "no information available",

                "not provided in the context",

                "not mentioned in the context"

            ]

            if any(

                pattern in answer_lower

                for pattern in fallback_patterns

            ):

                logger.info(
                    "LLM returned fallback response."
                )

                answer = self.FALLBACK_RESPONSE

            # ------------------------------------------------
            # Collect Source Information
            # ------------------------------------------------

            logger.info(
                "Collecting source metadata..."
            )

            sources = []

            for chunk in retrieved_chunks:

                sources.append(

                    {

                        "chunk_id": chunk["chunk_id"],

                        "document": chunk["document"],

                        "page": chunk["page"],

                        "distance": round(
                            chunk["distance"],
                            4
                        ),

                        # Used by Streamlit for preview
                        "text": chunk["text"]

                    }

                )

            logger.info(
                "Collected %d source records.",
                len(sources)
            )

            # ------------------------------------------------
            # Return Final Response
            # ------------------------------------------------

            logger.info("=" * 80)
            logger.info("RAG PIPELINE COMPLETED SUCCESSFULLY")
            logger.info("=" * 80)

            return {

                "success": True,

                "question": question,

                "answer": answer,

                "chunks_used": len(retrieved_chunks),

                "sources": sources

            }

        # ----------------------------------------------------
        # Exception Handling
        # ----------------------------------------------------

        except Exception as error:

            logger.exception(
                "Exception occurred during RAG pipeline execution."
            )

            return {

                "success": False,

                "question": question,

                "answer": None,

                "chunks_used": 0,

                "sources": [],

                "error": str(error)

            }

    # ========================================================
    # Document Summarization
    # ========================================================

    def summarize(
        self,
        context: str
    ) -> dict:

        try:

            logger.info("=" * 80)
            logger.info("DOCUMENT SUMMARIZATION")
            logger.info("=" * 80)

            logger.info(
                "Received document with %d characters.",
                len(context)
            )

            logger.info(
                "Building summarization prompt..."
            )

            prompt = self.prompt_builder.build_summary_prompt(
                context=context
            )

            if DEBUG:

                logger.info("=" * 80)
                logger.info("SUMMARY PROMPT")
                logger.info("=" * 80)
                logger.info(prompt)
                logger.info("=" * 80)

            logger.info(
                "Sending prompt to LLM..."
            )

            summary = self.llm_service.generate(
                prompt
            )

            logger.info(
                "Summary received successfully."
            )

            summary = summary.strip()

            if DEBUG:

                logger.info("=" * 80)
                logger.info("SUMMARY")
                logger.info("=" * 80)
                logger.info(summary)
                logger.info("=" * 80)

            return {

                "success": True,

                "summary": summary,

                "context_length": len(context)

            }

        except Exception as error:

            logger.exception(
                "Document summarization failed."
            )

            return {

                "success": False,

                "summary": None,

                "context_length": 0,

                "error": str(error)

            }

    # ========================================================
    # Generic Prompt Execution
    # ========================================================

    def generate(
        self,
        prompt: str
    ) -> dict:
        """
        Execute a prompt directly against the LLM.

        Used for:
        ----------
        • Prompt testing
        • Debugging
        • Prompt engineering
        • Direct LLM access
        """

        try:

            logger.info("=" * 80)
            logger.info("GENERIC PROMPT EXECUTION")
            logger.info("=" * 80)

            logger.info(
                "Received prompt (%d characters).",
                len(prompt)
            )

            if DEBUG:

                logger.info("=" * 80)
                logger.info("PROMPT")
                logger.info("=" * 80)
                logger.info(prompt)
                logger.info("=" * 80)

            logger.info(
                "Sending prompt to LLM..."
            )

            start_time = time.time()

            response = self.llm_service.generate(
                prompt
            )

            elapsed = round(
                time.time() - start_time,
                2
            )

            logger.info(
                "LLM response received in %.2f seconds.",
                elapsed
            )

            response = response.strip()

            if DEBUG:

                logger.info("=" * 80)
                logger.info("LLM RESPONSE")
                logger.info("=" * 80)
                logger.info(response)
                logger.info("=" * 80)

            return {

                "success": True,

                "response": response,

                "response_time": elapsed

            }

        except Exception as error:

            logger.exception(
                "Generic prompt execution failed."
            )

            return {

                "success": False,

                "response": None,

                "response_time": 0,

                "error": str(error)

            }

        