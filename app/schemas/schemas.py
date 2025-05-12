from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    category: str
    price: float

class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int

    class Config:
        orm_mode = True



class InventoryBase(BaseModel):
    product_id: int
    stock: int

class InventoryUpdate(BaseModel):
    stock: int

class InventoryOut(InventoryBase):
    id: int

    class Config:
        orm_mode = True


from datetime import datetime

class SaleBase(BaseModel):
    product_id: int
    quantity: int

class SaleOut(SaleBase):
    id: int
    total_price: float
    sold_at: datetime

    class Config:
        orm_mode = True

class RevenueSummary(BaseModel):
    period: str
    total_revenue: float
