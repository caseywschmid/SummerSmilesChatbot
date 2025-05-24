from .link import Link
from pydantic import BaseModel, Field


class Links(BaseModel):
    """
    Links model for the links field in the options object.
    Used in Options.
    """

    dealers: Link = Field(..., description="Dealers link")
    contact: Link = Field(..., description="Contact link")
    homepage_pool: str = Field(..., description="Homepage pool URL")
    homepage_spa: str = Field(..., description="Homepage spa URL")
    shop_products_pool: str = Field(..., description="Shop products pool URL")
    shop_products_spa: str = Field(..., description="Shop products spa URL")
