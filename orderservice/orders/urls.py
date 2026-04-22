# from django.urls import path
# from .views import add_cart, view_cart, create_order, checkout

# urlpatterns = [
#     path('add-cart/', add_cart),
#     path('view-cart/', view_cart),
#     path('create-order/', create_order),
#     path('checkout/', checkout),
# ]

from django.http import HttpResponse
from django.urls import path
from .views import add_cart, view_cart, create_order, order_history

def home(request):
    return HttpResponse("Orders Service Running 🚀")

urlpatterns = [
    path('', home),  # 👈 THIS FIX
    path('add-cart/', add_cart),
    path('view-cart/', view_cart),
    path('create-order/', create_order),
    path('history/', order_history),
]