import base64
import uuid


def generate_id(prefix: str) -> str:
    return f"{prefix}_{base64.urlsafe_b64encode(uuid.uuid4().bytes).decode().rstrip('=').lower()}"