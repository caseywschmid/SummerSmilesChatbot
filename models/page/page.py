from pydantic import BaseModel, Field, model_validator
from typing import List, Dict, Any, Optional, Union
from ..common.menu import Menu
from ..common.dealer_list_item import DealerListItem
from ..common.analytics import Analytics
from .block import Blocks
from ..common.options import Options
from ..common.seo import SEO
from ..common.fields import Fields


class Page(BaseModel):
    """
    Complete Page model for the response from Summer Smiles website.
    Represents a single page object in the API response.
    Used for parsing the 'pages' list in the API response.
    """

    type: str = Field(..., description="Type of the page")
    id: int = Field(..., description="ID of the page")
    title: str = Field(..., description="Title of the page")
    name: str = Field(..., description="Name of the page")
    homepage: bool = Field(..., description="Is this the homepage?")
    lang: str = Field(..., description="Language of the page")
    link: str = Field(..., description="Link to the page")
    langLinks: Dict[str, str] = Field(
        ..., description="Dictionary of language links for the page"
    )
    contentGroups: Optional[Union[List[Any], Dict[str, Any]]] = None
    footerMenu: Menu = Field(..., description="Footer menu object")
    mainMenu: Menu = Field(
        ..., description="Main menu object (same structure as footer menu)"
    )
    dealerList: List[DealerListItem] = Field(
        ..., description="List of dealer list items"
    )
    fields: Union[Fields, List] = Field(..., description="Fields object")
    analytics: Optional[Analytics] = Field(None, description="Analytics object")
    blocks: Blocks = Field(
        ..., description="Blocks object (mapping of block keys to block data)"
    )
    options: Options = Field(
        ..., description="Options object (site-wide options and settings)"
    )
    seo: SEO = Field(..., description="SEO object")

    @model_validator(mode="before")
    def fix_blocks_and_fields(cls, values):
        # Fix blocks
        blocks = values.get("blocks")
        if isinstance(blocks, list):
            values["blocks"] = {}
        elif isinstance(blocks, dict):
            # Fix fields in each block
            for block in blocks.values():
                if isinstance(block.get("fields"), list):
                    block["fields"] = {}
        return values
