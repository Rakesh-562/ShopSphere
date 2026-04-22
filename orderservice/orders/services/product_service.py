import requests
from django.conf import settings

def get_product(product_id):
    try:
        url = f"{settings.PRODUCT_SERVICE_URL}/products/{product_id}"

        res = requests.get(url, timeout=2)

        if res.status_code != 200:
            return None

        return res.json()

    except requests.exceptions.RequestException:
        return None
def reduce_stock(product_id, quantity):
    try:
        url = f"{settings.PRODUCT_SERVICE_URL}/products/{product_id}/reduce-stock"

        res = requests.post(url, json={"quantity": quantity}, timeout=2)

        if res.status_code != 200:
            return False

        return True

    except requests.exceptions.RequestException:
        return False