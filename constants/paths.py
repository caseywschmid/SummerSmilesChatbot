import os

FRENCH_PAGES_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "content/french/pages"
)
ENGLISH_PAGES_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "content/english/pages"
)

FRENCH_POSTS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "content/french/posts"
)
ENGLISH_POSTS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "content/english/posts"
)

FRENCH_PRODUCTS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "content/french/products"
)
ENGLISH_PRODUCTS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "content/english/products"
)

VECTOR_STORE_ID_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "constants/vector_store_ids.json",
)
