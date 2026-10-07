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

        try:
            Repo.clone_from(
                repo_url,
                destination,
                depth=1
            )
        except Exception as e:
            err_msg = str(e)
            if "not found" in err_msg.lower():
                raise ValueError(
                    f"Repository not found: '{repo_url}'. Please verify the URL and ensure the repository is public."
                )
            elif "permission denied" in err_msg.lower() or "authentication failed" in err_msg.lower():
                raise ValueError(
                    f"Access denied to '{repo_url}'. Please ensure the repository is public."
                )
            else:
                raise ValueError(f"Failed to clone repository: {err_msg.strip()}")

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