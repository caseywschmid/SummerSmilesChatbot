from pydantic import BaseModel, Field
from typing import Optional, Union, List, Dict, Any

class Analytics(BaseModel):
    """
    Analytics model for the analytics field in the API response.
    Used in models/page.py as the type for the 'analytics' field.
    """
    content_group: str = Field(..., description="Content group of the page")
    page_type: Optional[str] = None
    page_category: Optional[str] = None
    page_subcategory: Optional[Union[str, bool]] = None 