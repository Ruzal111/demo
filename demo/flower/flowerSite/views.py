from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect, HttpResponse

from .forms import RegistrationForm, CreateOrderForm
from .models import *

def index(req):
    products = Product.objects.all().filter(amount__gte=0).order_by('-id')[:5]
    return render(req, 'index.html', context={'products': products})

def where(req):
    return render(req, 'where.html')

def catalog(req, order, filter):
    rows = Product.objects.all().order_by(order)
    if filter:
        rows = rows.filter(category__id=filter)
    category = Category.objects.all().order_by('name')
    if req.user.is_authenticated:
        for row in rows:
            cart = Cart.objects.filter(user=req.user, product=row).first()
            row.cart = cart.amount if cart else 0
    return render(req, 'catalog.html', context={'products': rows, 'categories': category, 'order': order, 'filter': filter})

def product_detail(req, id):
    row = Product.objects.get(pk=id)
    if req.user.is_authenticated:
        cart = Cart.objects.filter(user=req.user, product=row).first()
        row.cart = cart.amount if cart else 0
    return render(req, 'product_detail.html', context={'product': row})

def registration(req):
    if req.method == 'POST':
        form = RegistrationForm(req.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('login')
    else:
        form = RegistrationForm()
    return render(req, 'registration/registration.html', context={'form': form})

@login_required
def cart(req):
    products = Cart.objects.all().filter(user=req.user)
    return render(req, 'cart.html', context={'products': products})

@login_required
def cart_add(req, id):
    row = Cart.objects.all().filter(user=req.user, product=id)
    product = Product.objects.get(pk=id)
    if len(row):
        row = row[0]
        if row.amount >= product.amount:
            return HttpResponse("<span class='error-count'>Больше добавить нельзя! в корзине %s шт</span>" % row.amount)
        row.amount += 1
    else:
        row = Cart(user=req.user, product=product, amount=1)
    row.save()
    return HttpResponse("в корзине %s шт" % row.amount)

@login_required
def cart_sub(req, id):
    row = Cart.objects.all().filter(user=req.user, product=id)
    if len(row):
        row = row[0]
        if row.amount:
            row.amount -= 1
            row.save() if row.amount else row.delete()
            return HttpResponse("в корзине %s шт" % row.amount)
        return HttpResponse("<span class='error-count'>Товар в корзине отсутствует!</span>")

@login_required
def create_order(req):
    if req.method == 'POST':
        form = CreateOrderForm(req.POST)
        if req.user.check_password(req.POST['password']):
            order = Order(user=req.user)
            order.save()
            products = Cart.objects.all().filter(user=req.user)
            for p in products:
                op = OrderProduct(order=order, product=p.product, amount=p.amount)
                op.save()
                p.delete()
            return HttpResponseRedirect('orders')
        else:
            form.add_error('password', 'не верный пароль')
    else:
        form = CreateOrderForm()
    return render(req, 'create_order.html', context={'form': form})


@login_required
def orders(req):
    orders = Order.objects.all().filter(user=req.user).order_by('-date_create')
    return render(req, 'orders.html', context={'orders': orders})

@login_required
def delete_order(req, id):
    order = Order.objects.get(pk=id)
    return render(req, 'delete_order.html', context={'order': order})


@login_required
def delete_order_ok(req, id):
    order = Order.objects.get(pk=id)
    order.delete()
    return HttpResponseRedirect('/orders')

# Create your views here.
