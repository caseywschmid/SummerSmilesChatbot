from models.page.page import Page
from models.posts.post import Post
from models.products.product import Product

SUMMER_SMILES_API_BASE_URL = "https://api.summersmiles.com/wp-json/nxstar/v2"

ENDPOINTS = {
    "pages": {
        "url": f"{SUMMER_SMILES_API_BASE_URL}/all-pages",
        "model": Page,
        "response_key": "pages",
    },
    "posts": {
        "url": f"{SUMMER_SMILES_API_BASE_URL}/all-posts",
        "model": Post,
        "response_key": "articles",
    },
    "products": {
        "url": f"{SUMMER_SMILES_API_BASE_URL}/all-products",
        "model": Product,
        "response_key": "products",
    },
}
