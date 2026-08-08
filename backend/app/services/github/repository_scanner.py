from pathlib import Path

class RepositoryScanner:
    """
    Scans cloned repository and returns all its files as a Python list.
    """

    def scan_repository(self, repository_path:Path) -> list[Path]:
        if not repository_path.exists():
            raise FileNotFoundError(f"Repository not found : {repository_path}")

        if not repository_path.is_dir():
            raise ValueError(f"Repository path is not a directory : {repository_path}")
        
        files = []

        for path in repository_path.rglob("*"):
            if path.is_file():
                files.append(path)
        
        return files