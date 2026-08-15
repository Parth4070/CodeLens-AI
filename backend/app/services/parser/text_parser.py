from pathlib import Path

from app.services.parser.base_parser import BaseParser


class TextParser(BaseParser):
    """
    Parser for plain-text and documentation files.
    """

    def parse(self, file_path: Path) -> dict:

        source_code = file_path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        return {
            "file_path": str(file_path),
            "language": "text",
            "content": source_code,
        }