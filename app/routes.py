from fastapi import APIRouter
from app.elastic import es
import uuid

router = APIRouter()

# ✅ GET ALL PRODUCTS
@router.get("/products")
def get_products():
    response = es.search(
        index="products",
        body={"query": {"match_all": {}}}
    )
    products = [hit["_source"] for hit in response["hits"]["hits"]]
    return products


# ✅ ADD PRODUCT (WITH UNIQUE ID)
@router.post("/products")
def add_product(product: dict):
    product_id = str(uuid.uuid4())   # unique id
    es.index(index="products", id=product_id, document=product)
    return {"message": "Product added successfully"}


# ✅ SEARCH PRODUCTS
@router.get("/products/search")
def search_products(query: str):
    response = es.search(
        index="products",
        body={
            "query": {
                "match": {
                    "name": {
                        "query": query,
                        "fuzziness": "AUTO"
                    }
                }
            }
        }
    )
    
    products = [hit["_source"] for hit in response["hits"]["hits"]]
    return products