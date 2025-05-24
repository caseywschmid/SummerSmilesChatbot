from pydantic import BaseModel, Field
from .link import Link


class ErrorPage(BaseModel):
    """
    ErrorPage model for the error_page field in the options object.
    Used in Options.
    """

    message: str = Field(..., description="Error message image URL")
    error_404: str = Field(..., alias="404", description="404 image URL")
    background: str = Field(..., description="Background image URL")
    background_mobile: str = Field(..., description="Background mobile image URL")
    link: Link = Field(..., description="Return to home link")
