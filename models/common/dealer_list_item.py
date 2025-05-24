from pydantic import BaseModel, Field
from .dealer import Dealer

class DealerListItem(BaseModel):
    """
    DealerListItem model for the dealerList field in the API response.
    Used in models/page.py as the type for items in the 'dealerList' field.
    """
    dealer: Dealer = Field(..., description="Dealer object") 