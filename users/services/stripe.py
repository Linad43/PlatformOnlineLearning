import stripe

from django.conf import settings


stripe.api_key = settings.STRIPE_API_KEY


def create_product(course):
    product = stripe.Product.create(
        name=course.title,
        description=course.description,
    )

    return {
        'id': product.id,
        'name': product.name,
        'description': product.description,
    }

def create_price(product_id, amount):
    price = stripe.Price.create(
        product=product_id,
        unit_amount=int(amount * 100),
        currency='rub',
    )

    return {
        'id': price.id,
        'product': price.product,
        'unit_amount': price.unit_amount,
        'currency': price.currency,
    }

def create_checkout_session(price_id):
    session = stripe.checkout.Session.create(
        mode='payment',
        line_items=[
            {
                'price': price_id,
                'quantity': 1,
            },
        ],
        success_url='http://127.0.0.1:8000/api/payments/success/',
        cancel_url='http://127.0.0.1:8000/api/payments/cancel/',
    )

    return {
        'id': session.id,
        'url': session.url,
    }