from pydantic import BaseModel
from typing import Optional, Dict, List

class Product(BaseModel):
    product_id: Optional[str] = None

    name: str
    brand: str
    category: str
    subcategory: Optional[str] = None

    price: float
    discount_price: Optional[float] = None

    stock: int
    rating: Optional[float] = 0

    image_url: Optional[str] = None
    description: Optional[str] = None

    specifications: Optional[Dict[str, str]] = {}
    tags: Optional[List[str]] = []