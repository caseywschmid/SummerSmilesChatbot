from openai import OpenAI
from openai.types import VectorStore
import logging
from services.logger import configure_logging

log = configure_logging(__name__, log_level=logging.DEBUG)


def load_vector_stores(client: OpenAI = None) -> list[VectorStore]:
    """
    Load all vector store objects from the OpenAI API.
    Step-by-step:
    1. Instantiate OpenAI client if not provided.
    2. List all vector stores via the API, handling pagination.
    3. Collect all vector store objects in a list.
    4. Return the list of vector store objects.
    You can later filter or map this list as needed for IDs, names, etc.
    """
    all_vector_stores = []
    page = client.vector_stores.list(limit=100)
    while True:
        all_vector_stores.extend(page.data)
        if hasattr(page, "has_next_page") and page.has_next_page:
            try:
                page = page.get_next_page()
            except Exception:
                break
        else:
            break
    log.debug(f"Loaded {len(all_vector_stores)} vector stores from OpenAI API.")
    log.debug(f"Vector stores: {[store.name for store in all_vector_stores]}")
    return all_vector_stores
