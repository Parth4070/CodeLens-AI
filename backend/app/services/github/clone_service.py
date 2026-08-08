from pathlib import Path
import shutil

from git import Repo


class CloneService:
    """
    Responsible for cloning Git repositories.
    """

    WORKSPACE = Path("workspace")

    def __init__(self):
        self.WORKSPACE.mkdir(exist_ok=True)

    def clone_repository(self, repo_url: str) -> Path:
        repo_name = repo_url.rstrip("/").split("/")[-1]

        if repo_name.endswith(".git"):
            repo_name = repo_name[:-4]

        destination = self.WORKSPACE / repo_name

        if destination.exists():
            self._remove_directory(destination)

        Repo.clone_from(
            repo_url,
            destination,
            depth=1
        )

        git_directory = destination / ".git"

        if git_directory.exists():
            self._remove_directory(git_directory)

        return destination

    @staticmethod
    def _remove_directory(path: Path):
        """
        Remove a directory while handling read-only files.
        """

        def on_error(func, path, exc_info):
            import os
            import stat

            os.chmod(path, stat.S_IWRITE)
            func(path)

        shutil.rmtree(
            path,
            onerror=on_error
        )