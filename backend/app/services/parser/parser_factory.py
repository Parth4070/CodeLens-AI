from pathlib import Path

from app.services.parser.base_parser import BaseParser
from app.services.parser.text_parser import TextParser
from app.services.parser.python_parser import PythonParser

class ParserFactory:
    @staticmethod
    def get_parser(file_path: Path) -> BaseParser:
        extension = file_path.suffix.lower()
        if extension == ".py":
            return PythonParser()
        else:
            raise ValueError(f"Unsupported file type: {extension}")
    
    CODE_EXTENSIONS = {
        ".py",
    }

    TEXT_EXTENSIONS = {
        ".md",
        ".txt",
        ".json",
        ".yaml",
        ".yml",
        ".toml",
    }

    TEXT_FILENAMES = {
        "README",
        "LICENSE",
        "Dockerfile",
        "Makefile",
    }

    @staticmethod
    def get_parser(file_path: Path) -> BaseParser:

        extension = file_path.suffix.lower()

        if extension in ParserFactory.CODE_EXTENSIONS:
            return PythonParser()

        if extension in ParserFactory.TEXT_EXTENSIONS:
            return TextParser()

        if file_path.name in ParserFactory.TEXT_FILENAMES:
            return TextParser()

        raise ValueError(
            f"Unsupported file type: {extension or file_path.name}"
        )