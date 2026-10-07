from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.utils.logger import logger

from app.services.github.clone_service import CloneService
from app.services.github.repository_service import RepositoryService
from app.services.indexing.indexing_service import IndexingService

router = APIRouter(
    prefix="/github",
    tags=["GitHub"]
)

_clone_service = None
_repository_service = None
_indexing_service = None


def get_clone_service() -> CloneService:
    global _clone_service
    if _clone_service is None:
        _clone_service = CloneService()
    return _clone_service


def get_repository_service() -> RepositoryService:
    global _repository_service
    if _repository_service is None:
        _repository_service = RepositoryService()
    return _repository_service


def get_indexing_service() -> IndexingService:
    global _indexing_service
    if _indexing_service is None:
        _indexing_service = IndexingService()
    return _indexing_service


class CloneRepositoryRequest(BaseModel):
    repo_url: str


@router.post("/clone")
async def clone_repository(
    request: CloneRepositoryRequest
):
    try:
        clone_service = get_clone_service()
        indexing_service = get_indexing_service()

        path = clone_service.clone_repository(
            request.repo_url
        )

        documents = indexing_service.index_repository(path)

        return {
            "repository": path.name,
            "repo_id": path.name,
            "path": str(path),
            "document_count": len(documents),
            "status": "indexed"
        }

    except ValueError as e:
        logger.warning(f"Repository validation/clone issue: {e}")
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        logger.exception(f"Unexpected error in clone_repository: {e}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get("/scan/{repository_name}")
async def scan_repository(repository_name: str):
    clone_service = get_clone_service()
    repository_service = get_repository_service()

    repository_path = (
        clone_service.WORKSPACE / repository_name
    )

    try:
        files = repository_service.get_source_files(
            repository_path
        )

        return {
            "repository": repository_name,
            "file_count": len(files),
            "files": [
                str(file.relative_to(repository_path))
                for file in files
            ]
        }

    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Repository not found"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )