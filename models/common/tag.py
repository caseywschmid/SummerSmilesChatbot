from pydantic import BaseModel, Field

class Tag(BaseModel):
    """
    Tag model for tag objects (e.g., in a tags list in API responses).
    Represents taxonomy/tag data as received from the API.
    """
    term_id: int = Field(..., description="Unique identifier for the term")
    name: str = Field(..., description="Name of the tag")
    slug: str = Field(..., description="Slug for the tag (URL-friendly)")
    term_group: int = Field(..., description="Term group identifier")
    term_taxonomy_id: int = Field(..., description="Unique identifier for the term taxonomy")
    taxonomy: str = Field(..., description="Taxonomy type (e.g., 'post_tag')")
    description: str = Field(..., description="Description of the tag")
    parent: int = Field(..., description="Parent term ID (0 if none)")
    count: int = Field(..., description="Count of posts with this tag")
    filter: str = Field(..., description="Filter type (e.g., 'raw')") 