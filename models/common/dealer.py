from pydantic import BaseModel, Field
from typing import Optional


class Dealer(BaseModel):
    """Dealer model for the response from Summer Smiles website."""

    id: int = Field(..., description="ID of the dealer")
    lat: str = Field(..., description="Latitude of the dealer")
    lng: str = Field(..., description="Longitude of the dealer")
    name: str = Field(..., description="Name of the dealer")
    street: str = Field(..., description="Street address of the dealer")
    city: str = Field(..., description="City of the dealer")
    state: str = Field(..., description="State of the dealer")
    postal_code: str = Field(..., description="Postal code of the dealer")
    categories: list[str] = Field(
        ..., description="List of categories associated with the dealer"
    )
    online_shop: Optional[str] = Field(None, description="Online shop link for the dealer")
    client_number: Optional[str] = Field(None, description="Client number of the dealer")
