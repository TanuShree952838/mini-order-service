from pydantic import BaseModel, Field
from typing import List


class OrderItemSchema(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)

    class Config:
        schema_extra = {
            "example": {
                "product_id": 1,
                "quantity": 3
            }
        }


class OrderSchema(BaseModel):
    items: List[OrderItemSchema]

    class Config:
        schema_extra = {
            "example": {
                "items": [
                    {"product_id": 1, "quantity": 3},
                    {"product_id": 2, "quantity": 1}
                ]
            }
        }

class ProductOut(BaseModel):
    id: int
    name: str
    price: float
    stock: int

    class Config:
        orm_mode = True
