import sys
from services.ai.openai_service import OpenAIService


def main():
    """
    Script to create or update a vector store for English or French content.
    """
    if sys.argv[1] not in (
        "SummerSmiles_English",
        "SummerSmiles_English_DEV",
        "SummerSmiles_French",
        "SummerSmiles_French_DEV",
    ):
        print(
            "Usage: python create_vector_store.py [SummerSmiles_English|SummerSmiles_French]"
        )
        sys.exit(1)
    name = sys.argv[1]
    service = OpenAIService()
    vector_store = service.get_vector_store_by_name(name)
    if vector_store:
        response = input(
            f"Vector store '{name}' already exists. If you choose to continue, it will be deleted and replaced with a new one of the same name.\nDo you want to continue? (y/N): "
        )
        if response.strip().lower() != "y":
            print("Operation cancelled by user.")
            sys.exit(0)
        deleted_vector_store = service.client.vector_stores.delete(
            vector_store_id=vector_store.id
        )
        print("deleted vector store")
    service.upload_files_to_vector_store(name)
    vector_store = service.get_vector_store_by_name(name)
    print(f"Vector store for '{name}' is ready. ID: {vector_store.id}")


if __name__ == "__main__":
    main()
