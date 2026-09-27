from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.github.clone_service import CloneService
from app.services.github.repository_service import RepositoryService
from app.services.indexing.indexing_service import IndexingService

router = APIRouter(
    prefix="/github",
    tags=["GitHub"]
)

clone_service = CloneService()
repository_service = RepositoryService()
indexing_service = IndexingService()

class CloneRepositoryRequest(BaseModel):
    repo_url: str


@router.post("/clone")
async def clone_repository(
    request: CloneRepositoryRequest
):
    try:
        path = clone_service.clone_repository(
            request.repo_url
        )

        documents = indexing_service.index_repository(path)

        return {
            "repository": path.name,
            "repo_id":path.name,
            "path": str(path),
            "document_count":len(documents),
            "status":"indexed"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get("/scan/{repository_name}")
async def scan_repository(repository_name: str):

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