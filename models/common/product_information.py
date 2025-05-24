from pydantic import BaseModel, Field
from typing import List, Optional, Union
from pydantic import field_validator

class ProductCharacteristic(BaseModel):
    """
    ProductCharacteristic model for each item in the characteristics list.
    Used in ProductInformation.
    """
    characteristics_title: str = Field(..., description="Title of the characteristic section")
    characteristics_data: str = Field(..., description="HTML content for the characteristic section")

class DosageRow(BaseModel):
    """
    DosageRow model for each row in a dosage column.
    Used in DosageColumn.
    """
    data: str = Field(..., description="HTML content for the dosage row")

class DosageColumn(BaseModel):
    """
    DosageColumn model for each column in the dosage table.
    Used in Dosage.
    """
    name: str = Field(..., description="Name of the dosage column")
    rows: Union[List[DosageRow], bool]

    @field_validator('rows', mode='before')
    def handle_false_as_empty_list(cls, v):
        if v is False:
            return []
        return v

class Dosage(BaseModel):
    """
    Dosage model for the dosage field in product information.
    Used in ProductInformation.
    """
    specifications: str = Field(..., description="HTML content for dosage specifications")
    columns: List[DosageColumn] = Field(..., description="List of columns for the dosage table")

    @field_validator('columns', mode='before')
    def handle_false_as_empty_list(cls, v):
        if v is False:
            return []
        return v

class ProductInformation(BaseModel):
    """
    ProductInformation model for the product_information field in the API response.
    Represents product characteristics, dosage, and warning information.
    """
    characteristics: List[ProductCharacteristic] = Field(..., description="List of product characteristics")
    dosage: Dosage = Field(..., description="Dosage information")
    warning: Optional[str] = Field("", description="Warning information (may be empty)")
