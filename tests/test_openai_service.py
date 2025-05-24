import pytest
from services.ai.openai_service import OpenAIService

# Instantiate the service once for all tests
service = OpenAIService()


def test_get_english_vector_store_by_name():
    """
    Test that fetching a vector store by name returns the correct object.
    """
    name = "SummerSmiles_English"
    vector_store = service.get_vector_store_by_name(name)
    assert vector_store is not None
    assert vector_store.name == name
    print(vector_store)


def test_get_french_vector_store_by_name():
    """
    Test that fetching a vector store by name returns the correct object.
    """
    name = "SummerSmiles_French"
    vector_store = service.get_vector_store_by_name(name)
    assert vector_store is not None
    assert vector_store.name == name
    print(vector_store)
