from pathlib import Path
from git import Repo
from app.utils.logger import logger
import shutil

class CloneService:
    """
    Clones Git repositeries.
    """

    WORKSPACE = Path("workspace")

    def __init__(self):
        """
        Initialize the CloneService.
        """
        self.WORKSPACE.mkdir(exist_ok=True)

    def clone_repository(self, url:str) -> Path:
        """
        Clone a Git repository.

        Args:
            url: The URL of the Git repository.

        Returns:
            The path to the cloned repository.
        """
        try:
            logger.info(f"Cloning repository: {url}")
            repo_name = url.rstrip("/").split("/")[-1]
            if repo_name.endswith(".git"):
                repo_name = repo_name[:-4]
            repo_path = self.WORKSPACE / repo_name

            if repo_path.exists():
                shutil.rmtree(repo_path)

            Repo.clone_from(url, repo_path)
            logger.info(f"Repository cloned successfully: {repo_path}")
            return repo_path
        except Exception as e:
            logger.error(f"Failed to clone repository: {e}")
            raise