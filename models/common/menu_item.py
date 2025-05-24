from pydantic import BaseModel, Field
from typing import List, Optional


class MenuItem(BaseModel):
    """Menu Item model for a menu."""

    menuId: int = Field(..., description="ID of the associated menu")
    lang: str = Field(..., description="Language of the menu item")
    id: int = Field(..., description="ID of the menu item")
    child_items: List["MenuItem"] = Field(
        ..., description="List of child items associated with the menu item"
    )
    menu_item_parent: str = Field(..., description="Parent ID of the menu item")
    title: str = Field(..., description="Title of the menu item")
    type: str = Field(..., description="Type of the menu item")
    important_link: bool = Field(..., description="Is this an important link?")
    super_category: Optional[str] = Field(
        None, description="Super category of the menu item"
    )
    url: str = Field(..., description="URL of the menu item")
