import os
from openai import OpenAI

from constants import (
    FRENCH_PAGES_PATH,
    ENGLISH_PAGES_PATH,
    ENGLISH_POSTS_PATH,
    FRENCH_POSTS_PATH,
    ENGLISH_PRODUCTS_PATH,
    FRENCH_PRODUCTS_PATH,
)

from services.ai.utils.create_vector_store import create_vector_store
from services.ai.utils.get_vector_store_by_name import get_vector_store_by_name
import logging
from services.logger import configure_logging

log = configure_logging(__name__, log_level=logging.DEBUG)


def upload_files_to_vector_store(client: OpenAI, name: str):
    """
    Upload all content files for the specified language to the corresponding vector store. If the specified vector store does not exist, it will be created.

    Note on chunking strategy:
    - max_chunk_size_tokens: Required[int] - The maximum number of tokens in each chunk. The default value is `800`. The minimum value is `100` and the maximum value is
    `4096`.
    - chunk_overlap_tokens: Required[int] - The number of tokens that overlap between chunks. The default value is `400`. Note that the overlap must not exceed half of `max_chunk_size_tokens`.
    """
    if name == "SummerSmiles_English" or name == "SummerSmiles_English_DEV":
        dir_paths = [ENGLISH_PAGES_PATH, ENGLISH_POSTS_PATH, ENGLISH_PRODUCTS_PATH]
    elif name == "SummerSmiles_French" or name == "SummerSmiles_French_DEV":
        dir_paths = [FRENCH_PAGES_PATH, FRENCH_POSTS_PATH, FRENCH_PRODUCTS_PATH]
    else:
        raise ValueError(f"Vector store name '{name}' does not match expected format.")

    vector_store = get_vector_store_by_name(client, name)
    if vector_store:
        client.vector_stores.delete(vector_store_id=vector_store.id)
        log.info("deleted vector store")
    vector_store = create_vector_store(client, name)
    for dir_path in dir_paths:
        log.info(f"Uploading files from {dir_path}")
        if not os.path.exists(dir_path):
            raise ValueError(f"Directory '{dir_path}' does not exist.")
        if not os.path.isdir(dir_path):
            raise ValueError(f"Path '{dir_path}' is not a directory.")
        for filename in os.listdir(dir_path):
            if filename.endswith(".json"):
                log.fine(f"Uploading file {filename}")
                file_path = os.path.join(dir_path, filename)
                with open(file_path, "rb") as file_content:
                    file_result = client.files.create(
                        file=file_content, purpose="assistants"
                    )
                client.vector_stores.files.create(
                    vector_store_id=vector_store.id,
                    file_id=file_result.id,
                    chunking_strategy={
                        "type": "static",
                        "static": {
                            "chunk_overlap_tokens": 400,
                            "max_chunk_size_tokens": 800,
                        },
                    },
                )
