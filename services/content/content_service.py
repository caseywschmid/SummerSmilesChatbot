import os
import json
import shutil
from typing import List, Dict, Any
from bs4 import BeautifulSoup
from models.page.page import Page
from services.api.summer_smiles_api_service import SummerSmilesAPIService
from utils import sanitize_filename, remove_unusual_line_terminators
from constants import (
    FRENCH_PAGES_PATH,
    ENGLISH_PAGES_PATH,
    FRENCH_POSTS_PATH,
    FRENCH_PRODUCTS_PATH,
    ENGLISH_POSTS_PATH,
    ENGLISH_PRODUCTS_PATH,
)
import logging
from services.logger import configure_logging

log = configure_logging(__name__, log_level=logging.DEBUG)


class ContentService:
    """
    Service for extracting and saving content from Summer Smiles pages.
    """

    def __init__(self, api_service: SummerSmilesAPIService = None):
        """
        Initialize the ContentService with an API service dependency.
        """
        self.api_service = api_service or SummerSmilesAPIService()

    @staticmethod
    def extract_text_blocks(page: Page) -> List[Dict[str, Any]]:
        """
        Recursively extract all 'text' fields from the blocks of a page using the Pydantic models.
        For each HTML block, also parse and extract the plain text using BeautifulSoup.
        Returns a list of dicts: { 'html': ..., 'text': ... }
        """

        def find_text_fields(obj):
            """
            Recursively search for 'text' fields in a nested dict or list.
            Returns a list of dicts: { 'text': ... }
            """
            content = []
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if k == "text" and isinstance(v, str):
                        soup = BeautifulSoup(v, "html.parser")
                        plain_text = soup.get_text(separator=" ", strip=True)
                        content.append({"text": plain_text})
                    else:
                        content.extend(find_text_fields(v))
            elif isinstance(obj, list):
                for item in obj:
                    content.extend(find_text_fields(item))
            return content

        all_content = []
        blocks_dict = page.blocks.root
        for block in blocks_dict.values():
            fields = block.fields
            all_content.extend(find_text_fields(fields))
        return all_content

    # TODO: add the related products to the pages
    def extract_and_save_all_pages_content(self) -> None:
        """
        Fetch all pages from the API and save the content to a JSON file.
        """
        os.makedirs(FRENCH_PAGES_PATH, exist_ok=True)
        os.makedirs(ENGLISH_PAGES_PATH, exist_ok=True)
        pages = self.api_service.get_all_pages()
        for page in pages:
            name = page.name
            link = page.link
            lang = page.lang
            content = self.extract_text_blocks(page)
            # Filter out blocks where both html and text are empty strings
            content = [
                block
                for block in content
                if not (block.get("html", "") == "" and block.get("text", "") == "")
            ]
            if not content:
                continue  # Skip pages with no text content
            for block in content:
                if "text" in block:
                    block["text"] = remove_unusual_line_terminators(block["text"])
            data = {"name": name, "link": link, "lang": lang, "content": content}
            filename = sanitize_filename(name) + ".json"
            if lang == "en":
                filepath = os.path.join(ENGLISH_PAGES_PATH, filename)
            elif lang == "fr":
                filepath = os.path.join(FRENCH_PAGES_PATH, filename)
            else:
                raise ValueError(f"Unknown language: {lang}")
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

    def extract_and_save_all_posts_content(self) -> None:
        """
        Fetch all posts from the API and save the content to a JSON file per post.
        """
        os.makedirs(FRENCH_POSTS_PATH, exist_ok=True)
        os.makedirs(ENGLISH_POSTS_PATH, exist_ok=True)
        posts = self.api_service.get_all_posts()
        for post in posts:
            name = post.name
            link = post.link
            lang = post.lang
            date = getattr(post, "date", None)
            title = getattr(post, "title", None)
            html_content = post.fields.content or ""
            soup = BeautifulSoup(html_content, "html.parser")
            plain_text = soup.get_text(separator=" ", strip=True)
            plain_text = remove_unusual_line_terminators(plain_text)
            data = {
                "name": name,
                "link": link,
                "lang": lang,
                "date": date,
                "title": title,
                "content": {"text": plain_text},
            }
            filename = sanitize_filename(name) + ".json"
            if lang == "en":
                filepath = os.path.join(ENGLISH_POSTS_PATH, filename)
            elif lang == "fr":
                filepath = os.path.join(FRENCH_POSTS_PATH, filename)
            else:
                raise ValueError(f"Unknown language: {lang}")
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

    # TODO: Add recommended levels to this
    def extract_and_save_all_products_content(self) -> None:
        """
        Fetch all products from the API and save the content to a JSON file per product.
        """
        os.makedirs(FRENCH_PRODUCTS_PATH, exist_ok=True)
        os.makedirs(ENGLISH_PRODUCTS_PATH, exist_ok=True)
        products = self.api_service.get_all_products()
        for product in products:
            name = product.name
            link = product.link
            lang = product.lang
            date = getattr(product, "date", None)
            title = getattr(product, "title", None)
            sku = getattr(product.fields, "sku", None)

            plain_long_description = ""
            long_description_soup = BeautifulSoup(
                getattr(product.fields, "long_description", None), "html.parser"
            )
            if long_description_soup:
                plain_long_description = long_description_soup.get_text(
                    separator=" ", strip=True
                )
                plain_long_description = remove_unusual_line_terminators(
                    plain_long_description
                )

            plain_short_description = ""
            short_description_soup = BeautifulSoup(
                getattr(product.fields, "short_description", None), "html.parser"
            )
            if short_description_soup:
                plain_short_description = short_description_soup.get_text(
                    separator=" ", strip=True
                )
                plain_short_description = remove_unusual_line_terminators(
                    plain_short_description
                )

            # --- Characteristics ---
            characteristics = []
            char_list = getattr(
                getattr(product.fields, "product_information", None),
                "characteristics",
                None,
            )
            if char_list:
                for char in char_list:
                    # Extract plain text from HTML
                    char_text = BeautifulSoup(
                        char.characteristics_data or "", "html.parser"
                    ).get_text(separator=" ", strip=True)
                    characteristics.append(
                        {
                            "title": char.characteristics_title,
                            "text": remove_unusual_line_terminators(char_text),
                        }
                    )

            # --- Dosage ---
            dosage_data = getattr(
                getattr(product.fields, "product_information", None), "dosage", None
            )
            dosage = None
            if dosage_data:
                # Extract plain text from specifications
                spec_text = BeautifulSoup(
                    getattr(dosage_data, "specifications", ""), "html.parser"
                ).get_text(separator=" ", strip=True)
                columns = []
                for col in getattr(dosage_data, "columns", []):
                    rows = []
                    for row in getattr(col, "rows", []):
                        row_text = BeautifulSoup(
                            getattr(row, "data", ""), "html.parser"
                        ).get_text(separator=" ", strip=True)
                        rows.append(remove_unusual_line_terminators(row_text))
                    columns.append({"name": getattr(col, "name", ""), "rows": rows})
                dosage = {
                    "specifications": remove_unusual_line_terminators(spec_text),
                    "columns": columns,
                }

            # --- Warning ---
            warning = getattr(
                getattr(product.fields, "product_information", None), "warning", None
            )
            if warning:
                warning = remove_unusual_line_terminators(
                    BeautifulSoup(warning, "html.parser").get_text(
                        separator=" ", strip=True
                    )
                )

            # --- Related Products ---
            # Extract related products using the updated RelatedProduct model structure
            related_products = []
            rel_list = getattr(product.fields, "related_products", None)
            if rel_list:
                for rel in rel_list:
                    # Access the RelatedProduct model attributes
                    rel_fields = getattr(rel, "fields", None)
                    rel_name = getattr(rel_fields, "name", None) if rel_fields else None
                    rel_link = getattr(rel, "permalink", None)
                    if rel_name and rel_link:
                        related_products.append({"name": rel_name, "link": rel_link})

            # --- Compose data dict ---
            data = {
                "title": title,
                "link": link,
                "lang": lang,
                "date": date,
                "long_description": plain_long_description,
                "short_description": plain_short_description,
                "characteristics": characteristics,
                "dosage": dosage,
                "warning": warning,
                "sku": sku,
                "related_products": related_products,
            }
            filename = sanitize_filename(name) + ".json"
            if lang == "en":
                filepath = os.path.join(ENGLISH_PRODUCTS_PATH, filename)
            elif lang == "fr":
                filepath = os.path.join(FRENCH_PRODUCTS_PATH, filename)
            else:
                raise ValueError(f"Unknown language: {lang}")
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

    def delete_all_content(self) -> None:
        """
        Delete the entire top-level 'content' folder (including all subfolders and files) to prepare for a fresh download.
        """
        # Get the parent directory of the English and French content paths (i.e., the 'content' directory)
        content_dir = os.path.dirname(os.path.dirname(FRENCH_PAGES_PATH))
        if os.path.exists(content_dir):
            shutil.rmtree(content_dir)
        # Recreate the empty content directory structure if needed for downstream code
        os.makedirs(FRENCH_PAGES_PATH, exist_ok=True)
        os.makedirs(ENGLISH_PAGES_PATH, exist_ok=True)
        os.makedirs(FRENCH_POSTS_PATH, exist_ok=True)
        os.makedirs(ENGLISH_POSTS_PATH, exist_ok=True)
        os.makedirs(FRENCH_PRODUCTS_PATH, exist_ok=True)
        os.makedirs(ENGLISH_PRODUCTS_PATH, exist_ok=True)
