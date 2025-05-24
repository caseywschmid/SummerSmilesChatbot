from pydantic import BaseModel, Field


class Link(BaseModel):
    """
    Link model for various link fields in the options object.
    Used in Options, Navbar, Footer, etc.
    """

    title: str = Field(..., description="Title of the link")
    url: str = Field(..., description="URL of the link")
    target: str = Field(..., description="Target attribute for the link")
