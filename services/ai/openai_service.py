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
from constants.ai import (
    OPENAI_MODEL,
    MODEL_COST_INPUT,
    MODEL_COST_OUTPUT,
    MODEL_COST_CACHED,
)
from openai.types.responses import Response, ResponseOutputMessage
from openai.types.responses.response_output_text import (
    Annotation,
    AnnotationFileCitation,
    AnnotationFilePath,
)

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

    def _parse_response(self, response: Response):
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        cached_tokens = response.usage.input_tokens_details.cached_tokens

        response_data = {
            "files": [],
            "input_tokens": input_tokens,
            "cached_tokens": cached_tokens,
            "output_tokens": output_tokens,
            "cost": 0.0,  # In USD
        }
        if response.output:
            for item in response.output:
                if isinstance(item, ResponseOutputMessage):
                    content = item.content
                    for i in content:
                        annotations = i.annotations
                        for annotation in annotations:
                            if isinstance(
                                annotation, AnnotationFileCitation
                            ) or isinstance(annotation, AnnotationFilePath):
                                # This is not listed on the model but is returned by the API
                                filename = annotation.filename
                                response_data["files"].append(filename)
        # Calculate the cost
        cost = 0
        cost += input_tokens * MODEL_COST_INPUT
        cost += output_tokens * MODEL_COST_OUTPUT
        cost += cached_tokens * MODEL_COST_CACHED
        response_data["cost"] = round(
            cost / 1000_000, 5
        )  # Convert to dollars per million tokens, rounded to 5 decimal places
        log.debug(f"Response: {response.model_dump_json(indent=2)}")
        log.info(f"Response data: {response_data}")
        return response_data

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
        response: Response = self.client.responses.create(**kwargs)
        response_data = self._parse_response(response)
        output_text = getattr(response, "output_text", str(response))
        response_id = getattr(response, "id", None)
        return output_text, response_id, response_data

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
