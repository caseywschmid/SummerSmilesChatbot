from services.ai.openai_service import OpenAIService
import sys
from services.logger import configure_logging

log = configure_logging(__name__, log_level="DEBUG")


def main():
    # Step 1: Check if the user provided a command-line argument for the vector store name
    if len(sys.argv) < 2:
        log.warn("Usage: python list_vector_store_files.py [VECTOR_STORE_NAME]")
        sys.exit(1)
    # Step 2: Validate the provided vector store name
    if sys.argv[1] not in (
        "SummerSmiles_English",
        "SummerSmiles_English_DEV",
        "SummerSmiles_French",
        "SummerSmiles_French_DEV",
    ):
        log.warn("Usage: python list_vector_store_files.py [VECTOR_STORE_NAME]")
        sys.exit(1)
    name = sys.argv[1]
    service = OpenAIService()
    vector_store = service.get_vector_store_by_name(name)
    if not vector_store:
        log.error(f"Vector store '{name}' not found.")
        sys.exit(1)

    # Fetch all files using pagination
    all_files = []
    after = None
    while True:
        page = service.client.vector_stores.files.list(
            vector_store_id=vector_store.id, limit=100, after=after
        )
        all_files.extend(page.data)
        if not page.has_next_page or not page.data:
            break
        after = page.data[-1].id  # Use the last file's ID as the cursor

    for f in all_files:
        log.debug(f)
    log.info(f"Number of files in vector store '{name}': {len(all_files)}")


if __name__ == "__main__":
    main()
