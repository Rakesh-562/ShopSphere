import redis
import json
import logging

logger = logging.getLogger(__name__)

# Attempt to connect to Redis
try:
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    r.ping() # Verify connection
except redis.ConnectionError:
    logger.warning("Redis is not running. Falling back to in-memory dictionary cart.")
    r = None

# Fallback cart
_fallback_cart = {}

def add_to_cart(user_id, product_id, quantity):
    if not r:
        key = str(user_id)
        if key not in _fallback_cart:
            _fallback_cart[key] = {}
            
        _fallback_cart[key][str(product_id)] = _fallback_cart[key].get(str(product_id), 0) + int(quantity)
        return True
        
    key = f"cart:{user_id}"
    cart = r.get(key)

    if cart:
        cart = json.loads(cart)
    else:
        cart = {}

    cart[str(product_id)] = cart.get(str(product_id), 0) + int(quantity)
    
    # TTL-based expiry of 1 hour (3600 seconds)
    r.setex(key, 3600, json.dumps(cart))
    return True


def get_cart(user_id):
    if not r:
        return _fallback_cart.get(str(user_id), {})
        
    data = r.get(f"cart:{user_id}")
    return json.loads(data) if data else {}

def clear_cart(user_id):
    if not r:
        if str(user_id) in _fallback_cart:
            del _fallback_cart[str(user_id)]
        return
        
    if r:
        r.delete(f"cart:{user_id}")