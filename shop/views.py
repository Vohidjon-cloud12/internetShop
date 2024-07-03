from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from pyexpat.errors import messages

from shop.forms import CommentModelForm, CommentModelForm, OrderForm, ProductForm, RegisterForm, LoginForm
from shop.models import Product, Category, Comment, CustomUser


# Create your views here.
def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(name__icontains=search_query)
    filter_expensive = request.GET.get('expensive')
    filter_cheap = request.GET.get('cheap')
    if filter_expensive:
        products = products.order_by('-price')[:2]
    elif filter_cheap:
        products = products.order_by('price')[:2]
    context = {'products': products,
               'categories': categories,
               'search_query': search_query,
               }
    return render(request, 'shop/home.html', context)


def details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.filter(category=product.category).exclude(id=product_id)
    comments = product.comments.all()
    return render(request, 'shop/detail.html',
                  context={'product': product, 'comments': comments, 'related_products': related_products})


def product_of_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    filter_expensive = request.GET.get('expensive')
    filter_cheap = request.GET.get('cheap')
    if filter_expensive:
        products = products.order_by('-price')[:2]
    elif filter_cheap:
        products = products.order_by('price')[:2]

    context = {'products': products}
    return render(request, 'shop/category_product.html', context)


def about(request):
    return render(request, 'shop/about.html')


# def comment_add(request, product_id):
#     product = Product.objects.get(id=product_id)
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             name = form.cleaned_data['name']
#             email = form.cleaned_data['email']
#             comment = form.cleaned_data['comment']
#             comment = Comment(name=name, email=email, comment=comment)
#             comment.product = product
#             comment.save()
#
#             return redirect('product_detail', product_id)
#     form = CommentForm()
#     comments = Comment.objects.all()
#     context = {'comments': comments, 'form': form}
#     return render(request, 'shop/detail.html', context)

def add_comment(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = CommentModelForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)

            comment.product = product
            comment.save()

            return redirect('product_detail', product.id)
    else:
        form = CommentModelForm(request.GET)

    return render(request, 'shop/detail.html', {'form': form, 'product': product})


def add_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            order.save()
            return redirect('product_detail', product.id)

    context = {'form': form, 'product': product}
    return render(request, 'shop/detail.html', context)


def add_product(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            return redirect('home')

    context = {'form': form}

    return render(request, 'shop/add-product.html', context)


def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'shop/update-product.html', context)


def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    return redirect('home')



def login_page(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('home')
    context = {'form': form}
    return render(request, 'shop/auth/login.html', context)


def logout_page(request):
    if request.method == 'POST':
        logout(request)
    return render(request, 'shop/auth/logout.html', )


def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            user = CustomUser.objects.create_user(username=username, email=email, password=password)
            user.is_active = True
            user.is_staff = True
            user.save()
            login(request, user)
            return redirect('home')
    context = {'form': form}

    return render(request, 'shop/auth/register.html', context )