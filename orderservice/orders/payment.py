import stripe
from django.conf import settings

# This should eventually be settings.STRIPE_SECRET_KEY
stripe.api_key = "sk_test_your_key"

def create_checkout_session(amount, user_id):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'inr',
                'product_data': {'name': 'Order Payment'},
                'unit_amount': int(amount * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://localhost:8000/success',
        cancel_url='http://localhost:8000/cancel',
        client_reference_id=str(user_id),
        metadata={
            'user_id': user_id
        }
    )
    return session.url