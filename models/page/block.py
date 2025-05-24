from pydantic import BaseModel, Field, RootModel
from typing import Dict, Any

class Block(BaseModel):
    """
    Block model for the blocks field in the API response.
    Used in models/page.py as the type for the 'blocks' field.
    This is a flexible model to handle dynamic block types, with a mapping of block keys to block data.
    """
    blockName: str = Field(..., description="Name of the block type")
    fields: Dict[str, Any] = Field(..., description="Fields for the block")

class Blocks(RootModel[Dict[str, Block]]):
    """
    Blocks model for the blocks field in the API response.
    Used in models/page.py as the type for the 'blocks' field.
    This is a mapping of block keys to Block objects, using RootModel for Pydantic v2 compatibility.
    """
    pass 