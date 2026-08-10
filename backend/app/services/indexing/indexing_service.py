from pathlib import Path

from langchain_core.documents import Document
from app.utils.logger import logger

from app.services.github.repository_service import RepositoryService
from app.services.parser.parser_factory import ParserFactory
from app.services.chunking.code_chunker import CodeChunker

class IndexingService:
    """
    Orchestrates repository servicing.
    """

    def __init__(self):
        self.repository_service = RepositoryService()
        self.chunker = CodeChunker()

    def index_repository(self, repo_path: Path) -> list[Document]:
        logger.info(f"Indexing repository: {repo_path}")

        source_files = self.repository_service.get_source_files(repo_path)

        all_documents = []
        
        for file_path in source_files:
            try:
                parser = ParserFactory.get_parser(file_path)

                parsed_code = parser.parse(file_path)

                documents = self.chunker.create_documents(parsed_code)

                all_documents.extend(documents)

            except Exception as e:
                logger.error(
                    f"Failed to process {file_path}: {e}"
                )
        
        logger.info(
            f"Successfully indexed {len(all_documents)} documents"
        )

        return all_documents

            
       
            