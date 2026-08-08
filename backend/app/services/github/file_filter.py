from pathlib import Path


class FileFilter:
    """
    Determines which repository files should be processed.
    """

    IGNORED_DIRECTORIES = {
        ".git",
        ".venv",
        "venv",
        "env",
        "__pycache__",
        "node_modules",
        "dist",
        "build",
        "coverage",
        ".idea",
        ".vscode",
    }

    ALLOWED_EXTENSIONS = {
        ".py",
        ".js",
        ".jsx",
        ".ts",
        ".tsx",
        ".java",
        ".cpp",
        ".c",
        ".h",
        ".hpp",
        ".go",
        ".rs",
        ".md",
        ".txt",
        ".json",
        ".yaml",
        ".yml",
        ".toml",
    }

    ALLOWED_FILENAMES = {
        "README",
        "README.md",
        "README.txt",
        "LICENSE",
        "Makefile",
        "Dockerfile",
        "requirements.txt",
        "pyproject.toml",
        "package.json",
        "package-lock.json",
    }

    def should_include(self, path: Path) -> bool:
        if any(
            part in self.IGNORED_DIRECTORIES
            for part in path.parts
        ):
            return False

        if path.name in self.ALLOWED_FILENAMES:
            return True

        if path.suffix.lower() in self.ALLOWED_EXTENSIONS:
            return True

        return False

    def filter_files(self, files: list[Path]) -> list[Path]:
        return [
            file
            for file in files
            if self.should_include(file)
        ]