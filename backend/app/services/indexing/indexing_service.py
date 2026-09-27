from pathlib import Path

# pyrefly: ignore [missing-import]
from langchain_core.documents import Document
from app.utils.logger import logger

from app.services.github.repository_service import RepositoryService
from app.services.parser.parser_factory import ParserFactory
from app.services.chunking.code_chunker import CodeChunker
from app.services.chunking.text_chunker import TextChunker
from app.services.embeddings.huggingface_embedding import HuggingFaceEmbeddingsService
from app.services.vectorstore.qdrant_service import QdrantService

class IndexingService:
    """
    Orchestrates repository servicing.
    """

    def __init__(self):
        self.repository_service = RepositoryService()
        self.code_chunker = CodeChunker()
        self.text_chunker = TextChunker()

        self.embedding_service  = HuggingFaceEmbeddingsService()
        self.qdrant_service = QdrantService()
    
    def add_repo_id(self, documents:list[Document], repo_id:str) -> list[Document]:
        for document in documents:
            document.metadata["repo_id"] = repo_id

        return documents

    def index_repository(self, repo_path: Path) -> list[Document]:
        logger.info(f"Indexing repository: {repo_path}")

        source_files = self.repository_service.get_source_files(repo_path)

        all_documents = []
        
        for file_path in source_files:
            try:
                parser = ParserFactory.get_parser(file_path)

                parsed_document = parser.parse(file_path)

                if parsed_document["language"] == "python":

                    file_documents = (
                        self.code_chunker.create_documents(
                            parsed_document
                        )
                    )
                    file_documents  = self.add_repo_id(file_documents, repo_path.name)

                else:

                    file_documents = (
                        self.text_chunker.create_documents(
                            parsed_document
                        )
                    )
                    file_documents  = self.add_repo_id(file_documents, repo_path.name)

                all_documents.extend(file_documents)

            except Exception :
                raise

        
        logger.info(
            f"Successfully indexed {len(all_documents)} documents"
        )

        if all_documents:
            embeddings = self.embedding_service.embed_docs(all_documents)

            vector_size = len(embeddings[0])

            self.qdrant_service.create_collection(vector_size)

            self.qdrant_service.add_docs(
                documents=all_documents,
                embeddings=embeddings
            )

            logger.info(
                f"Stored {len(all_documents)} documents in Qdrant"
            )

        return all_documents
