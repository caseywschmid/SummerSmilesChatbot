from pydantic import BaseModel, Field
from typing import Dict, Any
from .link import Link
from .image import Image


class Navbar(BaseModel):
    """
    Navbar model for the navbar field in the options object.
    Used in Options.
    """

    tag_icon: Image = Field(..., description="Tag icon object (Logo model)")
    tagline: str = Field(..., description="Tagline text")
    contact: Link = Field(..., description="Contact link")
    dealer: Link = Field(..., description="Dealer link")
    logo: Image = Field(..., description="Logo object (Logo model)")
    logo_mobile: Image = Field(..., description="Mobile logo object (Logo model)")
