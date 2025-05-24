import pytest
from services.api.summer_smiles_api_service import SummerSmilesAPIService
from models.page.page import Page
from models.posts.post import Post
from models.products.product import Product

# Instantiate the service once for all tests
service = SummerSmilesAPIService()


def test_get_all_pages():
    """
    Test that fetching all pages returns a non-empty list of Page objects
    and that each object has expected fields.
    """
    pages = service.get_all_pages()
    assert isinstance(pages, list)
    assert len(pages) > 0
    for page in pages:
        assert isinstance(page, Page)
        # Check some required fields
        assert isinstance(page.id, int)
        assert isinstance(page.title, str)
        assert hasattr(page, "link")


def test_get_all_posts():
    """
    Test that fetching all posts returns a non-empty list of Post objects
    and that each object has expected fields.
    """
    posts = service.get_all_posts()
    assert isinstance(posts, list)
    assert len(posts) > 0
    for post in posts:
        assert isinstance(post, Post)
        assert hasattr(post, "id")
        assert hasattr(post, "title")


def test_get_all_products():
    """
    Test that fetching all products returns a non-empty list of Product objects
    and that each object has expected fields.
    """
    products = service.get_all_products()
    assert isinstance(products, list)
    assert len(products) > 0
    for product in products:
        assert isinstance(product, Product)
        assert hasattr(product, "id")
        assert hasattr(product, "title")


def test_invalid_endpoint_raises():
    """
    Test that requesting an invalid endpoint raises a ValueError.
    """
    with pytest.raises(ValueError):
        service._fetch("not-a-real-endpoint") 