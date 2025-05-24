import requests
from typing import List, Any, Type, Optional
from models.page.page import Page
from models.posts.post import Post
from models.products.product import Product
from constants import ENDPOINTS
import logging
from services.logger import configure_logging

log = configure_logging(__name__, log_level=logging.DEBUG)


class SummerSmilesAPIService:
    """
    Service for interacting with the Summer Smiles API.
    Handles fetching and parsing data from various endpoints.
    Extendable: add new endpoints/models by updating ENDPOINTS.
    """

    def _fetch(self, endpoint_key: str) -> Any:
        """
        Internal method to fetch data from a given endpoint.
        Returns parsed data (typed if model is available, else raw dict/list).
        """
        if endpoint_key not in ENDPOINTS:
            raise ValueError(f"Unknown endpoint: {endpoint_key}")
        url = ENDPOINTS[endpoint_key]["url"]
        model: Optional[Type] = ENDPOINTS[endpoint_key]["model"]
        response_key: str = ENDPOINTS[endpoint_key].get("response_key", endpoint_key)

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to fetch {endpoint_key}: {e}")

        data = response.json()

        if response_key not in data:
            raise RuntimeError(
                f"Expected key '{response_key}' not found in API response"
            )
        items = data[response_key]

        if model is not None:
            return [model.model_validate(item) for item in items]
        else:
            return items

    def get_all_pages(self) -> List[Page]:
        """
        Fetch all pages from the API and return as a list of Page models.
        Raises RuntimeError on network or parsing errors.
        """
        return self._fetch("pages")

    def get_all_posts(self) -> List[Post]:
        """
        Fetch all posts from the API and return as a list of dicts (until a model is defined).
        Raises RuntimeError on network or parsing errors.
        """
        return self._fetch("posts")

    def get_all_products(self) -> List[Product]:
        """
        Fetch all products from the API and return as a list of dicts (until a model is defined).
        Raises RuntimeError on network or parsing errors.
        """
        return self._fetch("products")
