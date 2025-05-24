from pydantic import BaseModel, Field
from typing import Dict, Optional, List, Union
from .image import Image
from .analytics import Analytics
from .product_image import ProductImage
from .product_information import ProductInformation
from .related_products import RelatedProduct


class Fields(BaseModel):
    """
    Fields model for the 'fields' field in the API response.
    Used in models/page.py as the type for the 'fields' field.
    Represents the structure of the fields object as received from the API.
    """

    title: Optional[str] = Field(None, description="Title of the post or page")
    image_or_video: Optional[str] = Field(
        None, description="Type indicator: 'image' or 'video'"
    )
    content: Optional[str] = Field(None, description="HTML content")
    poster: Optional[Union[Image, bool]] = Field(
        None, description="Poster image object"
    )  # If no poster, returns False
    product_category: Optional[List[int]] = Field(
        None, description="List of product category IDs"
    )
    video: Optional[str] = Field(None, description="Video URL (e.g., YouTube embed)")
    image: Optional[Union[Image, bool]] = Field(
        None, description="Image object"
    )  # If no image, returns False
    analytics: Optional[Analytics] = Field(None, description="Analytics object")
    product_image: Optional[Image] = Field(None, description="Product image object")
    format_images: Optional[
        Union[
            List[Dict[str, Union[Image, bool]]],  # list of dicts with Image or bool
            Dict[str, Union[Image, bool]],  # dict of str to Image or bool
            bool,
        ]
    ] = Field(None, description="List of format images")
    sku: Optional[str] = Field(None, description="Stock Keeping Unit (SKU)")
    long_description: Optional[str] = Field(
        None, description="Long description of the product"
    )
    short_description: Optional[str] = Field(
        None, description="Short description of the product"
    )
    product_icons: Optional[List[ProductImage]] = Field(
        None, description="List of product icons"
    )
    product_information: Optional[ProductInformation] = Field(
        None, description="Product information object"
    )
    related_products: Optional[List[RelatedProduct]] = Field(
        None, description="List of related product objects with fields and permalinks"
    )
