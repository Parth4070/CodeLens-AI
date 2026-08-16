import hashlib
import uuid

def generate_chunk_id(file_path:str, chunk_type: str, class_name: str= "", function_name: str = "") -> str:
    raw_id = "|".join([
        file_path,
        chunk_type,
        class_name,
        function_name
    ])

    hash_value = hashlib.sha256(raw_id.encode("utf-8")).hexdigest()

    deterministic_uuid = uuid.UUID(hash_value[:32])

    return str(deterministic_uuid)