# pyrefly: ignore [missing-import]
from langchain_core.prompts import ChatPromptTemplate

from app.models.rag import RAGResponse, Source
from app.services.rag.context_builder import ContextBuilder
# pyrefly: ignore [missing-import]
from app.services.retrieval.retrieval_service import RetrievalService
# pyrefly: ignore [missing-import]
from app.services.llm.llm_service import LLMService

class RAGService:
    def __init__(self):
        self.context_builder = ContextBuilder()
        self.retrieval_service = RetrievalService()
        self.llm_service = LLMService()

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    You are CodeLens, an AI assistant
                    that helps developers understand
                    software repositories.

                    Answer questions using ONLY the
                    provided repository context.

                    Rules:

                    1. Do not invent code or files.
                    2. If the context does not contain
                    enough information, say so.
                    3. Mention the relevant file paths.
                    4. Mention class/function names when
                    available.
                    5. Keep answers concise and technical.
                    """,
                ),
                ("human", 
               """Repository context:

                {context}

                Question:

                {question}
                """),
            ]
        )

    def ask(self, question:str, top_k: int=5) -> str:
        chunks = self.retrieval_service.search(query= question, limit=top_k)

        context = self.context_builder.build(chunks)

        messages = self.prompt.format_messages(
            context = context,
            question = question
        )

        prompt_text = "\n".join(message.content for message in messages)

        answer = self.llm_service.generate(prompt_text)

        sources = [Source(
            file_path = chunk.file_path,
            chunk_type = chunk.chunk_type,
            class_name = chunk.class_name,
            function_name = chunk.function_name,
            start_line = chunk.start_line,
            end_line = chunk.end_line,
            score = chunk.score,
        ) for chunk in chunks]

        return RAGResponse(
            answer = answer,
            sources = sources
        )