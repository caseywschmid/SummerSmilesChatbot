from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional, Union


class BubbleIconData(BaseModel):
    """
    BubbleIconData model for the icon object inside each bubble icon.
    Used in BubbleIcon (models/common/bubbles.py).
    Represents the structure of the icon data as received from the API.
    """
    ID: int = Field(..., description="Primary ID of the icon (may be duplicate of 'id')")
    id: int = Field(..., description="ID of the icon (may be duplicate of 'ID')")
    title: str = Field(..., description="Title of the icon")
    filename: str = Field(..., description="Filename of the icon image")
    filesize: int = Field(..., description="Filesize in bytes")
    url: str = Field(..., description="URL to the icon image")
    link: str = Field(..., description="Link to the icon's page")
    alt: str = Field(..., description="Alt text for the icon image")
    author: str = Field(..., description="Author ID or name")
    description: str = Field(..., description="Description of the icon")
    caption: str = Field(..., description="Caption for the icon")
    name: str = Field(..., description="Name of the icon")
    status: str = Field(..., description="Status of the icon")
    uploaded_to: int = Field(..., description="ID of the parent object the icon was uploaded to")
    date: str = Field(..., description="Upload date of the icon")
    modified: str = Field(..., description="Last modified date of the icon")
    menu_order: int = Field(..., description="Menu order for the icon")
    mime_type: str = Field(..., description="MIME type of the icon image")
    type: str = Field(..., description="Type of the icon (e.g., 'image')")
    subtype: str = Field(..., description="Subtype of the icon (e.g., 'svg+xml')")
    icon: str = Field(..., description="URL to the default icon image")
    width: Union[int, str] = Field(..., description="Width of the icon image (may be string or int)")
    height: Union[int, str] = Field(..., description="Height of the icon image (may be string or int)")
    sizes: Dict[str, Any] = Field(..., description="Dictionary of available image sizes and their URLs/metadata")


class BubbleIcon(BaseModel):
    """
    BubbleIcon model for each icon in the bubbles field in the options object.
    Used in Bubbles (models/common/bubbles.py).
    """
    icon: BubbleIconData = Field(..., description="Icon object for the bubble")


class Bubbles(BaseModel):
    """
    Bubbles model for the bubbles field in the options object.
    Used in Options (models/options.py).
    """
    icons: List[BubbleIcon] = Field(..., description="List of bubble icons")
