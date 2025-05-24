from pydantic import BaseModel, Field
from .link import Link


class CallToAction(BaseModel):
    """
    CallToAction model for the call_to_action field in the subscribe object.
    Used in Subscribe (models/common/subscribe.py).
    Represents the structure of the call_to_action data as received from the API.
    """

    link_type: str = Field(
        ..., description="Type of the call to action link (e.g., 'text')"
    )
    link: Link = Field(..., description="Link object for the call to action")
    image: bool = Field(..., description="Whether the call to action uses an image")
