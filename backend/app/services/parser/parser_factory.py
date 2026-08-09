from pathlib import Path

from app.services.parser.base_parser import BaseParser
from app.services.parser.python_parser import PythonParser

class ParserFactory:
    @staticmethod
    def get_parser(file_path: Path) -> BaseParser:
        extension = file_path.suffix.lower()
        if extension == ".py":
            return PythonParser()
        else:
            raise ValueError(f"Unsupported file type: {extension}")