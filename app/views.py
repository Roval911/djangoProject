from djangoProject.settings import STRIPE_SECRET_KEY
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
import stripe
from .models import *

stripe.api_key = STRIPE_SECRET_KEY


@csrf_exempt
def get_checkout_session(request, item_id):
    item = Item.objects.get(pk=item_id)

    # Перевод цены в центы
    price_cents = int(item.price * 100)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item.name,
                    'description': item.description,
                },
                'unit_amount': price_cents,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(item.get_absolute_url()),
        cancel_url=request.build_absolute_uri(item.get_absolute_url()),
    )

    return JsonResponse({'session_id': session.id})


def view_item(request, item_id):
    item = Item.objects.get(pk=item_id)
    return render(request, 'item_detail.html', {'item': item})


@csrf_exempt
def create_order(request, item_id):
    item = get_object_or_404(Item, pk=item_id)

    # Создать заказ с выбранным товаром
    order = Order.objects.create()
    order.items.add(item)

    # Прикрепите к заказу скидки и налоги (вы можете настроить эту логику)
    discount = Discount.objects.create(name='Promo', amount=5)
    tax = Tax.objects.create(name='VAT', rate=0.1)
    order.discounts.add(discount)
    order.taxes.add(tax)

    # Перевести общую стоимость в центы
    total_price_cents = int(order.total_price() * 100)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': f"Order #{order.id}",
                },
                'unit_amount': total_price_cents,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(order.get_absolute_url()),
        cancel_url=request.build_absolute_uri(order.get_absolute_url()),
    )

    order.payment_intent_id = session.payment_intent
    order.save()

    return JsonResponse({'session_id': session.id})


def view_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'order_detail.html', {'order': order})
