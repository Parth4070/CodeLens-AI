from pydantic import BaseModel


class RetrievedChunk(BaseModel):
    content: str
    file_path: str

    chunk_type: str

    class_name: str | None = None
    function_name: str | None = None

    start_line: int | None = None
    end_line: int | None = None

    score: float