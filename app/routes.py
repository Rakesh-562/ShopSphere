from fastapi import APIRouter, HTTPException
from app.elastic import es
from app.schemas import Product
import time

router = APIRouter()


# ✅ GET ALL PRODUCTS
@router.get("/products")
def get_products():
    response = es.search(
        index="products",
        body={"query": {"match_all": {}}},
        size=100
    )

    products = []
    for hit in response["hits"]["hits"]:
        product = hit["_source"]
        product["product_id"] = hit["_id"]
        products.append(product)

    return products


# ✅ SEARCH PRODUCTS (IMPORTANT: ABOVE ID ROUTE)
@router.get("/products/search")
def search_products(query: str):
    start_time = time.time()

    response = es.search(
        index="products",
        body={
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": [
                        "name^3",
                        "brand^2",
                        "category",
                        "subcategory",
                        "tags"
                    ],
                    "fuzziness": "AUTO"
                }
            }
        }
    )

    end_time = time.time()

    products = []
    for hit in response["hits"]["hits"]:
        product = hit["_source"]
        product["product_id"] = hit["_id"]
        products.append(product)

    return {
        "latency_ms": round((end_time - start_time) * 1000, 2),
        "results_count": response["hits"]["total"]["value"],
        "results": products
    }


# ✅ ADD PRODUCT (FIXED - USES YOUR product_id)
@router.post("/products")
def add_product(product: Product):
    if not product.product_id:
        raise HTTPException(status_code=400, detail="product_id is required")

    es.index(
        index="products",
        id=product.product_id,   # ✅ IMPORTANT FIX
        document=product.dict()
    )

    return {
        "message": "Product added successfully",
        "product_id": product.product_id
    }


# ✅ GET SINGLE PRODUCT (KEEP LAST)
@router.get("/products/{product_id}")
def get_product_by_id(product_id: str):
    try:
        response = es.get(index="products", id=product_id)
        product = response["_source"]
        product["product_id"] = response["_id"]
        return product
    except Exception:
        raise HTTPException(status_code=404, detail="Product not found")