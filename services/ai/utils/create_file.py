from openai import OpenAI

import logging
from services.logger import configure_logging

log = configure_logging(__name__, log_level=logging.DEBUG)

def create_file(client: OpenAI, file_path: str):
    """
    Create a file in OpenAI (for manual file upload, not used in vector store flow).
    """
    with open(file_path, "rb") as file_content:
        result = client.files.create(file=file_content, purpose="assistants")
    log.debug(result.id)
    return result.id
