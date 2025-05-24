from pydantic import BaseModel, Field
from typing import Dict, Any


class Image(BaseModel):
    """
    Represents the structure of image data as received from the API.
    """

    ID: int = Field(
        ..., description="Primary ID of the logo (may be duplicate of 'id')"
    )
    id: int = Field(..., description="ID of the logo (may be duplicate of 'ID')")
    title: str = Field(..., description="Title of the logo")
    filename: str = Field(..., description="Filename of the logo image")
    filesize: int = Field(..., description="Filesize in bytes")
    url: str = Field(..., description="URL to the logo image")
    link: str = Field(..., description="Link to the logo's page")
    alt: str = Field(..., description="Alt text for the logo image")
    author: str = Field(..., description="Author ID or name")
    description: str = Field(..., description="Description of the logo")
    caption: str = Field(..., description="Caption for the logo")
    name: str = Field(..., description="Name of the logo")
    status: str = Field(..., description="Status of the logo")
    uploaded_to: int = Field(
        ..., description="ID of the parent object the logo was uploaded to"
    )
    date: str = Field(..., description="Upload date of the logo")
    modified: str = Field(..., description="Last modified date of the logo")
    menu_order: int = Field(..., description="Menu order for the logo")
    mime_type: str = Field(..., description="MIME type of the logo image")
    type: str = Field(..., description="Type of the logo (e.g., 'image')")
    subtype: str = Field(..., description="Subtype of the logo (e.g., 'png')")
    icon: str = Field(..., description="URL to the default icon image")
    width: int = Field(..., description="Width of the logo image")
    height: int = Field(..., description="Height of the logo image")
    sizes: Dict[str, Any] = Field(
        ..., description="Dictionary of available image sizes and their URLs/metadata"
    )
