import pytest
from decimal import Decimal
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Order, OrderItem
from unittest.mock import patch

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def mock_user(db):
    return User.objects.create_user(username="testuser", password="password")

@pytest.mark.django_db
def test_add_cart_missing_product_id(api_client, mock_user):
    response = api_client.post('/orders/add-cart/', {"quantity": 1}, format='json')
    assert response.status_code == 400

@patch('orders.views.add_to_cart')
@pytest.mark.django_db
def test_add_cart_success(mock_add_cart, api_client, mock_user):
    # Mocking Redis to succeed
    mock_add_cart.return_value = True
    response = api_client.post('/orders/add-cart/', {"product_id": 99, "quantity": 2}, format='json')
    assert response.status_code == 200
    assert response.data["message"] == "Added to cart"
    mock_add_cart.assert_called_once_with(mock_user.id, 99, 2)

@patch('orders.views.get_cart')
@pytest.mark.django_db
def test_view_cart(mock_get_cart, api_client, mock_user):
    mock_cart_data = {"123": 2, "456": 1}
    mock_get_cart.return_value = mock_cart_data
    response = api_client.get('/orders/view-cart/')
    assert response.status_code == 200
    assert response.data == mock_cart_data
    mock_get_cart.assert_called_once_with(mock_user.id)

@patch('orders.views.get_cart')
@pytest.mark.django_db
def test_create_order_empty_cart(mock_get_cart, api_client, mock_user):
    mock_get_cart.return_value = {}
    response = api_client.post('/orders/create-order/')
    assert response.status_code == 400
    assert response.data["error"] == "Cart empty"

@patch('orders.views.get_cart')
@patch('orders.views.clear_cart')
@patch('orders.views.publish_order_event')
@pytest.mark.django_db
def test_create_order_success(mock_publish, mock_clear, mock_get_cart, api_client, mock_user):
    mock_get_cart.return_value = {"10": 2, "20": 1} # IDs: 10, 20
    response = api_client.post('/orders/create-order/')
    assert response.status_code == 201
    
    # Assert Order was created correctly
    orders = Order.objects.all()
    assert len(orders) == 1
    assert orders[0].user == mock_user
    # Total = 100 * 2 + 100 * 1 = 300.00
    assert orders[0].total_amount == Decimal("300.00")
    
    # Assert Order Items created
    items = OrderItem.objects.all()
    assert len(items) == 2
    
    # Ensure cart was cleared and event published
    mock_clear.assert_called_once_with(mock_user.id)
    mock_publish.assert_called_once_with(orders[0].id)

@pytest.mark.django_db
def test_order_history_pagination(api_client, mock_user):
    # Create 15 orders to test DRF pagination works accurately
    for i in range(15):
        Order.objects.create(user=mock_user, total_amount=Decimal('100.00'))
        
    response = api_client.get('/orders/history/')
    assert response.status_code == 200
    
    # The default page size is 10
    assert "count" in response.data
    assert response.data["count"] == 15
    assert len(response.data["results"]) == 10
    
    # Check page 2
    response_page2 = api_client.get('/orders/history/?page=2')
    assert response_page2.status_code == 200
    assert len(response_page2.data["results"]) == 5

@patch('orders.cart.r')
def test_cart_module_without_redis(mock_redis):
    # Test fallback correctly handles redis failure if none
    from orders.cart import add_to_cart, get_cart, clear_cart
    
    # Suppose global r is None
    import orders.cart
    orders.cart.r = None
    
    success = add_to_cart(1, 99, 1)
    assert not success
    assert get_cart(1) == {}
