import datetime

from django.http import JsonResponse
from django.shortcuts import render
import json

from .models import *
from .utils import cookie_cart, cart_data, guest_order


# Create your views here.


def store(request):
    products = Product.objects.all()
    data = cart_data(request)
    cart_items = data['cart_items']

    context = {
        'products': products,
        'cart_items': cart_items,
    }
    return render(request, 'store/store.html', context)


def cart(request):
	data = cart_data(request)
    cart_items = data['cart_items']
    order = data['order']
    items = data['items']

    context = {
        'items': items,
        'order': order,
        'cart_items': cart_items,
    }
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cart_data(request)
    cart_items = data['cart_items']
    order = data['order']
    items = data['items']

    context = {
        'items': items,
        'order': order,
        'cart_items': cart_items,
    }
    return render(request, 'store/checkout.html', context)


def update_item(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']
    print('product_id view: ',product_id)
    print('action view: ',action)

    customer = request.user.customer
    # lấy ra sản phẩm với id = product_id, product_id của data-product tại class name update-cart
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        order_item.quantity = (order_item.quantity + 1)
    elif action == 'remove':
        order_item.quantity = (order_item.quantity -1 )

    order_item.save()

    if order_item.quantity <= 0 or action == 'trash':
        order_item.delete()

    return JsonResponse("Item was updated!", safe=False)


def process_order(request):
    print("data: ", request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guest_order(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping:
        ShippingAddress.objects.create(
            customer=customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
        )

    return JsonResponse("Payment Completed !!!", safe=False)


def product_detail(request, pk):
    product = Product.objects.get(id=pk)

    data = cart_data(request)
    cart_items = data['cart_items']
    order = data['order']
    items = data['items']

    context = {
        'product': product,
        'items': items,
        'order': order,
        'cart_items': cart_items,
    }
    return render(request, 'store/product-detail.html', context)


def search(request):
    try:
        q = request.GET.get('q')
    except:
        q = None
    if q:
        products = Product.objects.filter(name__icontains=q)
        print(products)
        data = cart_data(request)
        cart_items = data['cart_items']
        context = {
            "query":q,
            'products':products,
            'cart_items': cart_items,
        }
        template = 'store/results.html'
    else:
        products = Product.objects.all()

        data = cart_data(request)
        cart_items = data['cart_items']

        context = {
            'products': products,
            'cart_items': cart_items,
        }
        template = 'store/store.html'
    return render(request, template, context)
