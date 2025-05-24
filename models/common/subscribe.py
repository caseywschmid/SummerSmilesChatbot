from pydantic import BaseModel, Field
from .call_to_action import CallToAction


class Subscribe(BaseModel):
    """
    Subscribe model for the subscribe field in the options object.
    Used in Options.
    """

    title: str = Field(..., description="Subscribe title")
    text: str = Field(..., description="Subscribe text")
    background_color: str = Field(..., description="Background color")
    call_to_action: CallToAction = Field(..., description="Call to action object")
