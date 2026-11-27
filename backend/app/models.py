from pydantic import BaseModel, Field


class Product(BaseModel):
    id: int
    name: str
    category: str
    price: float = Field(gt=0)
    stock_quantity: int = Field(ge=0)
    active: bool = True
