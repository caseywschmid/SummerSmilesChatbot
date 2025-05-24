from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional, Union

from .bubbles import Bubbles
from .error_page import ErrorPage
from .links import Links
from .footer import Footer
from .navbar import Navbar
from .subscribe import Subscribe


class Options(BaseModel):
    """
    Options model for the options field in the API response.
    Used in models/page.py as the type for the 'options' field.
    """

    bubbles: Bubbles = Field(..., description="Bubbles object")
    error_page: ErrorPage = Field(..., description="Error page object")
    footer: Footer = Field(..., description="Footer object")
    links: Links = Field(..., description="Links object")
    navbar: Navbar = Field(..., description="Navbar object")
    subscribe: Subscribe = Field(..., description="Subscribe object")
