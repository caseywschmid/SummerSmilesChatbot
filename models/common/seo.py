from pydantic import BaseModel, Field
from typing import Optional, Union

class SEO(BaseModel):
    """
    SEO model for the seo field in the API response.
    Used in models/page.py as the type for the 'seo' field.
    """
    title: str = Field(..., description="SEO title")
    description: str = Field(..., description="SEO description")
    image: Union[bool, str] = Field(..., description="SEO image (bool or URL)")
    follow: str = Field(..., description="SEO follow directive")
    index: str = Field(..., description="SEO index directive")
    canonical: str = Field(..., description="SEO canonical URL")
    og_title: str = Field(..., description="Open Graph title")
    og_description: str = Field(..., description="Open Graph description")
    og_image: bool = Field(..., description="Open Graph image (bool or URL)")
    twitter_title: str = Field(..., description="Twitter title")
    twitter_description: str = Field(..., description="Twitter description")
    twitter_image: bool = Field(..., description="Twitter image (bool or URL)") 