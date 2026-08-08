from pathlib import Path

from app.services.github.repository_scanner import RepositoryScanner
from app.services.github.file_filter import FileFilter

class RepositoryService:

    def __init__(self):
        self.scanner = RepositoryScanner()
        self.file_filter = FileFilter()

    def get_source_files(self, repository_path: Path) -> list[Path]:
        all_files = self.scanner.scan_repository(repository_path)

        source_files = self.file_filter.filter_files(all_files)

        return source_files