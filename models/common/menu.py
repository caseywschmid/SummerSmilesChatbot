from pydantic import BaseModel, Field
from models.common.menu_item import MenuItem


class Menu(BaseModel):
    """Menu model for the response from Summer Smiles website."""

    items: list[MenuItem] = Field(
        ..., description="List of menu items in the footer menu"
    )
    homepageUrl: str = Field(..., description="URL of the homepage")
