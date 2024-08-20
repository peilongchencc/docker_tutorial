from pydantic import BaseModel

# 数据模型
class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None