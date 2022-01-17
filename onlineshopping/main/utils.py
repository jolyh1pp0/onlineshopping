import json
from . models import *


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    items = []
    order = {'get_cart_total': 0, 'get_items_total': 0, 'get_cart_items': 0, 'shipping': True}
    cartItems = order['get_cart_items']
    for i in cart:
        try:
            cartItems += cart[i]['quantity']
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product': {
                    'id': product.id,
                    'title': product.title,
                    'model': product.model,
                    'price': product.price,
                    'stock': product.stock,
                },
                'quantity': cart[i]['quantity'],
                'get_total': total
            }
            items.append(item)

            if product.stock is False:
                order['shipping'] = False

        except:
            pass

    return {'cartItems': cartItems, 'order': order, 'items': items}


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        items = cookieData['items']
        order = cookieData['order']

    return {'cartItems': cartItems, 'order': order, 'items': items}


def guestOrder(request, data):
    name = data['form']['name']
    surname = data['form']['surname']
    email = data['form']['email']
    phone = data['form']['phone']

    cookieData = cookieCart(request)
    items = cookieData['items']
    Customer.objects.get_or_create(
        name=data['form']['name'],
        surname=data['form']['surname'],
        phone=data['form']['phone'],
        email=data['form']['email'],
    )
    customer, created = Customer.objects.get_or_create(
        name=name,
        email=email,
        surname=surname,
        phone=phone,
    )
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False,
    )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        model = Category.objects.get(id=product.id)
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product, quantity=item['quantity'])
        orderItem.model = model
        orderItem.save()

    return customer, order
