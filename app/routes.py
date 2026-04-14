from fastapi import APIRouter
from app.elastic import es
import uuid

router = APIRouter()

@router.get("/products")
def get_products():
    response = es.search(index="products", body={"query": {"match_all": {}}})
    return [hit["_source"] for hit in response["hits"]["hits"]]


@router.post("/products")
def add_product(product: dict):
    product_id = str(uuid.uuid4())
    es.index(index="products", id=product_id, document=product)
    return {"message": "Product added successfully"}


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
    return [hit["_source"] for hit in response["hits"]["hits"]]