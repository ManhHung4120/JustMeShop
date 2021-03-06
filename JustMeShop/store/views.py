import json
import datetime
from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from .utils import cookieCart,cartData


def store(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)


def cart(request):

	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):

	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quatity = (orderItem.quatity + 1)
	elif action == 'remove':
		orderItem.quatity = (orderItem.quatity - 1)

	orderItem.save()

	if orderItem.quatity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order.complete = True
        order.save()
    else:
        print('User is not logged in')
        print('COOKIES:', request.COOKIES)
        name = data['form']['name']
        email = data['form']['email']
        cookieData = cookieCart(request)
        items = cookieData['items']
        customer, created = Customer.objects.get_or_create(
				email=email,
				)
        customer.name = name
        customer.save()
        order = Order.objects.create(
			customer=customer,
			complete=False,
			)
        for item in items:
            product = Product.objects.get(id=item['id'])
            orderItem = OrderItem.objects.create(
				product=product,
				order=order,
				quatity=item['quatity'],
			)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        if total == order.total_all:
            order.complete = True
            order.save()
    
        Shipping.objects.create(
            customer = customer,
            order = order,
            address = data['form']['address'],
            city = data['form']['city']
            
        )
    
    return JsonResponse('Payment complete', safe=False)


