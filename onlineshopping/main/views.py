from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from . utils import cookieCart, cartData, guestOrder
import json
import datetime


def index(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    data = cartData(request)
    cartItems = data['cartItems']

    return render(request, 'main/index.html', {'title': 'Главная страница', 'products': products, 'categories': categories, 'cartItems': cartItems})


def cart(request):
    data = cartData(request)

    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

    return render(request, 'main/cart.html', {'title': 'Корзина', 'items': items, 'order': order, 'cartItems': cartItems})


def products(request):
    return render(request, 'main/products.html')


def order(request):
    data = cartData(request)

    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

    return render(request, 'main/order.html', {'title': 'Оформление заказа', 'items': items, 'order': order, 'cartItems': cartItems})


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productID']
    action = data['action']
    customer = request.user.customer

    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    model = Category.objects.get(id=productId)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.model = model
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = data['form']['total']
    order.transaction_id = transaction_id

    if int(total) == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingInformation.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zip_code=data['shipping']['zip_code'],
        )

        Receipt.objects.create(
            customer=customer,
            order=order,
            total_price=int(data['form']['total'])
        )

        global cust
        cust = customer

    return JsonResponse('Payment complete!', safe=False)


def receipt(request):
    orders = Order.objects.all()

    receipt = Receipt.objects.get(order_id=orders[::-1][0])
    items = OrderItem.objects.filter(order_id=orders[::-1][0])
    customer = Customer.objects.get(id=receipt.customer_id)

    return render(request, 'main/receipt.html', {'title': 'Чек', 'items': items, 'customer': customer, 'receipt': receipt})
