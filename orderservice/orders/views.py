from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from .services.product_service import get_product, reduce_stock
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User

from .models import Order, OrderItem
from .serializers import OrderSerializer
from .cart import add_to_cart, get_cart, clear_cart
from .producer import publish_order_event
from .utils.auth import get_user_from_request

def home(request):
    return HttpResponse("ShopSphere Order Service Running ")


@api_view(['POST'])
def add_cart(request):
    user = get_user_from_request(request)
    if not user:
        return Response({"error": "Unauthorized"}, status=401) # Using first user as mock Auth
    product_id = request.data.get("product_id")
    quantity = request.data.get("quantity", 1)

    if not product_id:
        return Response({"error": "product_id is required"}, status=400)

    success = add_to_cart(user.id, product_id, quantity)
    if success:
        return Response({"message": "Added to cart"})
    return Response({"error": "Failed to add to cart. Redis unavailable."}, status=503)


@api_view(['GET'])
def view_cart(request):
    user = get_user_from_request(request)
    if not user:
        return Response({"error": "Unauthorized"}, status=401)
    return Response(get_cart(user.id))

# Kept for backward compatibility or direct creation without payment
@api_view(['POST'])
def create_order(request):
    user = get_user_from_request(request)
    if not user:
        return Response({"error": "Unauthorized"}, status=401)

    cart = get_cart(user.id)

    if not cart:
        return Response({"error": "Cart empty"}, status=400)

    total = Decimal('0.00')
    items = []

    for product_id, qty in cart.items():
        product = get_product(product_id)

        if not product:
            return Response({"error": f"Product {product_id} not found"}, status=404)

        if product["stock"] < qty:
            return Response({"error": f"Product {product_id} out of stock"}, status=400)
        success = reduce_stock(product_id, qty)
        if not success:
            return Response({"error": "Stock update failed"}, status=500)
        price = Decimal(str(product["price"]))
        total += price * Decimal(qty)

        items.append({
            "product_id": int(product_id),
            "qty": qty,
            "price": price
        })

    # Create order
    order = Order.objects.create(user=user, total_amount=total)

    for item in items:
        OrderItem.objects.create(
            order=order,
            product_id=item["product_id"],
            quantity=item["qty"],
            price=item["price"]
        )

    clear_cart(user.id)
    publish_order_event(order.id)

    serializer = OrderSerializer(order)

    return Response({
        "message": "Order created",
        "order": serializer.data
    }, status=201)

from rest_framework.pagination import PageNumberPagination

@api_view(['GET'])
def order_history(request):
    user = get_user_from_request(request)
    if not user:
        return Response({"error": "Authentication required"}, status=401)
        
    orders = Order.objects.filter(user=user).order_by('-created_at')
    
    paginator = PageNumberPagination()
    paginator.page_size = 10 # 10 past orders per page
    result_page = paginator.paginate_queryset(orders, request)
    
    serializer = OrderSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)
