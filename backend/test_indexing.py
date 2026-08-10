from pathlib import Path

from app.services.indexing.indexing_service import (
    IndexingService
)


repository_path = Path(
    "workspace/AI-Research-Assistant-2"
)

indexing_service = IndexingService()

documents = indexing_service.index_repository(
    repository_path
)

print(f"\nTotal documents: {len(documents)}\n")

for document in documents:

    print("=" * 70)

    print("CONTENT:")
    print(document.page_content)

    print("\nMETADATA:")
    print(document.metadata)