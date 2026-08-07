from fastapi import APIRouter
from app.services.github.clone_service import CloneService
from app.utils.logger import logger
from pydantic import BaseModel

router = APIRouter(prefix="/github", tags=["Github"])

class CloneRequest(BaseModel):
    url: str

@router.post("/clone")
async def clone_repository(request: CloneRequest):
    logger.info("Cloning repository")
    service = CloneService()
    repo_path = service.clone_repository(request.url)
    logger.info(f"Repository cloned successfully: {repo_path}")
    return {
        "status": "success",
        "repo_path": str(repo_path),
        "repository":repo_path.name
    }