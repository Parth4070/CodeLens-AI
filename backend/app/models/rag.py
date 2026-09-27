from pydantic import BaseModel

class Source(BaseModel):
    file_path: str
    chunk_type: str

    class_name: str | None = None
    function_name: str | None = None

    start_line: int | None = None
    end_line: int | None = None

    rerank_score: float | None = None
    retrieval_score: float | None = None

class RAGResponse(BaseModel):
    answer: str
    sources: list[Source]

