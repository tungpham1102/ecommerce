from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from .decorator import unauthenticated_user

# Create your views here.
from store.utils import cart_data


@unauthenticated_user
def register(request):
    form = UserRegisterForm()
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account was created')
            return redirect('login')
    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Username or Password is incorrect")
            return redirect('login')

    return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    return redirect('login')


def validate_register(request):
    username = request.GET.get('username', None)
    email = request.GET.get('email', None)
    data = {
        'is_taken_username': User.objects.filter(username__iexact=username).exists(),
        'is_taken_email': User.objects.filter(email__iexact=email).exists()
    }

    if data['is_taken_username']:
        data['error_message_username'] = "A user with this name already exist"

    if data['is_taken_email']:
        data['error_message_email'] = "A user with this email already exist"
    return JsonResponse(data)


def user_page(request):
    data = cart_data(request)
    cart_items = data['cart_items']
    order = data['order']
    items = data['items']

    context = {
        'items': items,
        'order': order,
        'cart_items': cart_items,
    }
    return render(request, 'accounts/user-page.html', context)