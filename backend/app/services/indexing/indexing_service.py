from pathlib import Path

# pyrefly: ignore [missing-import]
from langchain_core.documents import Document
from app.utils.logger import logger

from app.services.github.repository_service import RepositoryService
from app.services.parser.parser_factory import ParserFactory
from app.services.chunking.code_chunker import CodeChunker
from app.services.chunking.text_chunker import TextChunker

class IndexingService:
    """
    Orchestrates repository servicing.
    """

    def __init__(self):
        self.repository_service = RepositoryService()
        self.code_chunker = CodeChunker()
        self.text_chunker = TextChunker()

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

                else:

                    file_documents = (
                        self.text_chunker.create_documents(
                            parsed_document
                        )
                    )

                all_documents.extend(file_documents)

            except Exception :
                raise

        
        logger.info(
            f"Successfully indexed {len(all_documents)} documents"
        )

        return all_documents

            
       
            