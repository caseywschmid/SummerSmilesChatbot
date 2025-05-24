from pydantic import BaseModel, Field
from typing import Dict, Any, Union

from .image import Image


class ProductImage(BaseModel):
    """
    Represents the structure of image data as received from the API.
    """

    name: str = Field(..., description="Name of the logo")
    icon: Union[Image, bool] = Field(
        ..., description="URL to the default icon image (Logo model)"
    )
    background_color: str = Field(
        ..., description="Background color of the image in hex format"
    )
