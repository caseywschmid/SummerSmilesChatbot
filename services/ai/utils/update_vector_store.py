from services.ai.utils import upload_files_to_vector_store


def update_vector_store(language: str):
    """
    Update the vector store for the specified language by re-uploading all files.
    (This can be improved to check for diffs, but for now, it re-uploads all.)
    """
    upload_files_to_vector_store(language)
