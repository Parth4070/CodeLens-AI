# pyrefly: ignore [missing-import]
from langchain_core.documents import Document
from app.utils.id_generator import generate_chunk_id

class TextChunker:
    """
    Converts text parser output into LangChain Documents.
    """

    def create_documents(
        self,
        parsed_document: dict
    ) -> list[Document]:

        document = Document(
            page_content=parsed_document["content"],
            metadata={
                "file_path": parsed_document["file_path"],
                "language": parsed_document["language"],
                "chunk_type": "document",
                "chunk_id": generate_chunk_id(
                    file_path=parsed_document["file_path"],
                    chunk_type="document"
                )
            },
        )

        return [document]