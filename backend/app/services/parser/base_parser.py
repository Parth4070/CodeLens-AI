from abc import ABC, abstractmethod
from pathlib import Path

class BaseParser(ABC):
    @abstractmethod
    def parse(self, file_path:Path) -> dict:
        """
        Parse a source code file and return its structure.

        Args:
            file_path: Path to the source code file

        Returns
            Dictionary containing the parsed structure
        """
        pass

    