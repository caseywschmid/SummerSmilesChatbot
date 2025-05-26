from openai import OpenAI
from dotenv import load_dotenv
import os
from typing import Optional
from services.ai.utils import (
    load_vector_stores as load_vector_stores,
    create_or_update_vector_store,
    upload_files_to_vector_store,
    get_vector_store_by_name,
    create_file,
)
from prompts.system_message import SYSTEM_MESSAGE
from constants.ai import OPENAI_MODEL

import logging
from services.logger import configure_logging


log = configure_logging(__name__, log_level=logging.DEBUG)
load_dotenv()


class OpenAIService:
    """
    Service for OpenAI integration, including:
    - Vector store management (create, update, upload files)
    - Language detection for routing
    - Chat integration with file search
    """

    def __init__(self):
        """
        Initialize the OpenAIService with API key and load or initialize vector store IDs.
        """
        api_key = os.environ["OPENAI_API_KEY"]
        self.client = OpenAI(api_key=api_key)
        self.vector_stores = self.load_vector_stores()
        self.vector_store_ids = {}
        for vector_store in self.vector_stores:
            self.vector_store_ids[vector_store.name] = vector_store.id

    def chat(
        self,
        user_input: str,
        previous_response_id: Optional[str] = None,
        name: Optional[str] = "SummerSmiles_English",
    ) -> tuple[str, str]:
        """
        Handle a chat request:
        """
        log.debug(f"Using vector store: {name}")
        vector_store_id = self.vector_store_ids[name]
        input_list = []
        input_list.append(
            {
                "role": "system",
                "content": SYSTEM_MESSAGE,
            }
        )
        input_list.append({"role": "user", "content": user_input})
        kwargs = {
            "model": OPENAI_MODEL,
            "input": input_list,
            "tools": [{"type": "file_search", "vector_store_ids": [vector_store_id]}],
        }
        if previous_response_id:
            kwargs["previous_response_id"] = previous_response_id
        response = self.client.responses.create(**kwargs)
        # TODO: add more robust response parsing
        log.debug(f"Response: {response.model_dump_json(indent=2)}")
        output_text = getattr(response, "output_text", str(response))
        response_id = getattr(response, "id", None)
        return output_text, response_id

    def load_vector_stores(self):
        return load_vector_stores(self.client)

    def create_or_update_vector_store(self, language: str):
        return create_or_update_vector_store(self.client, language)

    def update_vector_store(self, name: str):
        """
        (STAGED)
        Update the vector store for the specified language by re-uploading all files.
        (This can be improved to check for diffs, but for now, it re-uploads all.)
        """
        self.upload_files_to_vector_store(self.client, name)

    def upload_files_to_vector_store(self, language: str):
        """
        Upload files to a vector store.
        """
        return upload_files_to_vector_store(self.client, language)

    def get_vector_store_by_name(self, name: str):
        """
        Get a vector store by name.
        """
        return get_vector_store_by_name(self.client, name)

    def create_file(self, filepath: str):
        """
        Create a file in the vector store.
        """
        return create_file(self.client, filepath)
