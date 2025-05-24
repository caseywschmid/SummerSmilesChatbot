from pydantic import BaseModel, Field

from .link import Link
from .image import Image


class Footer(BaseModel):
    """
    Footer model for the footer field in the options object.
    Used in Options.
    """

    logo: Image = Field(..., description="Footer logo object")
    dealers: Link = Field(..., description="Dealers link")
    about: Link = Field(..., description="About link")
    contact_number: str = Field(..., description="Contact number")
    contact_page: Link = Field(..., description="Contact page link")
    follow_title: str = Field(..., description="Follow us title")
    facebook: str = Field(..., description="Facebook link")
    youtube: str = Field(..., description="YouTube link")
    copyright: str = Field(..., description="Copyright text")
    terms_of_use: Link = Field(..., description="Terms of use link")
    privacy_policy: Link = Field(..., description="Privacy policy link")
