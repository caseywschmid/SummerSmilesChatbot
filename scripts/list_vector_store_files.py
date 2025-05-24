from services.ai.openai_service import OpenAIService
import sys


def main():
    # Step 1: Check if the user provided a command-line argument for the vector store name
    if len(sys.argv) < 2:
        print("Usage: python list_vector_store_files.py [VECTOR_STORE_NAME]")
        sys.exit(1)
    # Step 2: Validate the provided vector store name
    if sys.argv[1] not in (
        "SummerSmiles_English",
        "SummerSmiles_English_DEV",
        "SummerSmiles_French",
        "SummerSmiles_French_DEV",
    ):
        print("Usage: python list_vector_store_files.py [VECTOR_STORE_NAME]")
        sys.exit(1)
    name = sys.argv[1]
    service = OpenAIService()
    vector_store = service.get_vector_store_by_name(name)
    if not vector_store:
        print(f"Vector store '{name}' not found.")
        sys.exit(1)

    vector_store_files = service.client.vector_stores.files.list(
        vector_store_id=vector_store.id
    )
    print(vector_store_files)


if __name__ == "__main__":
    main()
