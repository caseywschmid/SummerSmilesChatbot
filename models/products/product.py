from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union


from ..common.menu import Menu
from ..common.options import Options
from ..common.seo import SEO
from ..common.fields import Fields
from ..common.tag import Tag


class Product(BaseModel):
    """
    Complete Product model for the response from Summer Smiles website.
    Represents a single product/page object in the API response.
    Used for parsing the 'articles' list in the API response.
    """

    category: Optional[List[Tag]] = Field(
        None, description="List of category tags for the product"
    )
    contentGroups: Optional[Union[List[Any], Dict[str, Any]]] = None
    date: Optional[str] = Field(None, description="Date of the product")
    fields: Fields = Field(
        ..., description="Fields object (custom fields for the product)"
    )
    footerMenu: Menu = Field(..., description="Footer menu object")
    id: int = Field(..., description="ID of the page or product")
    lang: str = Field(..., description="Language of the page or product")
    langLinks: Dict[str, str] = Field(
        ..., description="Dictionary of language links for the page or product"
    )
    link: str = Field(..., description="Link to the page or product")
    mainMenu: Menu = Field(
        ..., description="Main menu object (same structure as footer menu)"
    )
    name: str = Field(..., description="Name of the page or product")
    options: Options = Field(
        ..., description="Options object (site-wide options and settings)"
    )
    seo: SEO = Field(..., description="SEO object")
    tags: Optional[Union[List[Tag], bool]] = Field(
        None, description="List of tags for the product"
    )  # If no tags, returns False
    title: str = Field(..., description="Title of the page or product")
    type: str = Field(..., description="Type of the page or product")
