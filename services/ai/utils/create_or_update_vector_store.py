from openai import OpenAI

from services.ai.utils import (
    load_vector_stores,
    get_vector_store_by_name,
    update_vector_store,
)
import logging
from services.logger import configure_logging


log = configure_logging(__name__, log_level=logging.DEBUG)


def create_or_update_vector_store(client: OpenAI, language: str) -> str:
    """
    Create a new vector store for the specified language ('en' or 'fr') if one does not exist.
    If a store with the intended name exists, log a warning and update it (re-upload files).
    Returns the vector store ID.
    """
    vector_store_ids = load_vector_stores()
    name = f"SummerSmiles_{'English' if language == 'en' else 'French'}"
    existing_vector_store = get_vector_store_by_name(client, name)
    if existing_vector_store:
        log.warn(
            f"Vector store '{name}' already exists (id: {existing_vector_store.id}). Will update it."
        )
        update_vector_store(language)
        return existing_vector_store.id
    else:
        vector_store = client.vector_stores.create(name=name)
        vector_store_ids[language] = vector_store.id
        return vector_store.id
