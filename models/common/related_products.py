from pydantic import BaseModel, Field
from typing import Optional
from .image import Image
from .analytics import Analytics


class RelatedProductFields(BaseModel):
    """
    Fields contained within each related product object.
    Used by RelatedProduct model to represent the nested fields structure.
    Contains product name, image, rating and analytics data.
    """
    name: Optional[str] = Field(None, description="Name of the related product")
    product_image: Optional[Image] = Field(None, description="Product image object")
    stars: Optional[int] = Field(None, description="Star rating of the product")
    analytics: Optional[Analytics] = Field(None, description="Analytics data for the product")


class RelatedProduct(BaseModel):
    """
    Model representing a related product object from the API.
    Used in models/common/fields.py for the related_products field.
    Each related product contains fields with product info and a permalink.
    """
    fields: Optional[RelatedProductFields] = Field(None, description="Product fields containing name, image, stars, and analytics")
    permalink: Optional[str] = Field(None, description="URL permalink to the related product page") 