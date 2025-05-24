from openai import OpenAI
from openai.types import VectorStore
import logging
from services.logger import configure_logging

log = configure_logging(__name__, log_level=logging.DEBUG)


def create_vector_store(client: OpenAI, name: str) -> VectorStore:
    """
    Create a new vector store in OpenAI.
    """
    vector_store = client.vector_stores.create(name=name)
    return vector_store
