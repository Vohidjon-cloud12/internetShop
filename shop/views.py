from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from pyexpat.errors import messages

from shop.forms import CommentForm
from shop.models import Product, Category, Comment


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
    return render(request, 'shop/detail.html', context={'product': product})


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


def comment_add(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            comment = form.cleaned_data['comment']
            comment = Comment(name=name, email=email, comment=comment)
            comment.product = product
            comment.save()

            return redirect('product_detail', product_id)
    form = CommentForm()
    comments = Comment.objects.all()
    context = {'comments': comments, 'form': form}
    return render(request, 'shop/detail.html', context)
