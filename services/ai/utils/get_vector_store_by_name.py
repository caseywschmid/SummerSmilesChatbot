from openai import OpenAI


def get_vector_store_by_name(client: OpenAI, name: str):
    """
    Check if a vector store with the given name exists.
    Returns the VectorStore object if found, else None.
    """
    page = client.vector_stores.list(limit=100)
    while True:
        for vs in page.data:
            if vs.name == name:
                return vs
        if page.has_next_page:
            try:
                page = page.get_next_page()
            except RuntimeError:
                break
        else:
            break
    return None
