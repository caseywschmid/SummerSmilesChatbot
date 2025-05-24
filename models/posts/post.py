from pydantic import BaseModel, Field, model_validator
from typing import List, Dict, Any, Optional, Union


from ..common.analytics import Analytics
from ..common.menu import Menu
from ..common.dealer_list_item import DealerListItem
from ..common.options import Options
from ..common.seo import SEO
from ..common.fields import Fields
from ..common.tag import Tag


class Post(BaseModel):
    """
    Complete Post model for the response from Summer Smiles website.
    Represents a single article/page object in the API response.
    Used for parsing the 'articles' list in the API response.
    """

    category: Optional[List[Tag]] = Field(
        None, description="List of category tags for the article"
    )
    contentGroups: Optional[Union[List[Any], Dict[str, Any]]] = None
    date: Optional[str] = Field(None, description="Date of the article")
    fields: Fields = Field(
        ..., description="Fields object (custom fields for the article)"
    )
    footerMenu: Menu = Field(..., description="Footer menu object")
    id: int = Field(..., description="ID of the page or article")
    lang: str = Field(..., description="Language of the page or article")
    langLinks: Dict[str, str] = Field(
        ..., description="Dictionary of language links for the page or article"
    )
    link: str = Field(..., description="Link to the page or article")
    mainMenu: Menu = Field(
        ..., description="Main menu object (same structure as footer menu)"
    )
    name: str = Field(..., description="Name of the page or article")
    options: Options = Field(
        ..., description="Options object (site-wide options and settings)"
    )
    seo: SEO = Field(..., description="SEO object")
    tags: Optional[Union[List[Tag], bool]] = Field(
        None, description="List of tags for the article"
    )  # If no tags, returns False
    title: str = Field(..., description="Title of the page or article")
    type: str = Field(..., description="Type of the page or article")
