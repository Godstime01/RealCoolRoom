from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import SignUpForm, BookingForm
from .models import BookingModel
from .task import test_func


# Create your views here.
def homepage(request):
    # test_func.delay()
    print(request.user.username)
    if request.user.is_authenticated and not request.user.is_staff:
        return redirect("dashboard")
    else:
        # return redirect("/admin")
        pass
    return render(request, 'index.html')


def register_request(request):

    if request.user.is_authenticated:
        return redirect("homepage")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("homepage")
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    form = SignUpForm()
    return render(request=request, template_name="forms/register.html", context={"register_form": form})


def login_request(request):

    if request.user.is_authenticated:
        return redirect("homepage")
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("homepage")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="forms/login.html", context={"login_form": form})


@login_required(login_url='/login')
def user_dashboard(request):
    
    print(request.user)
    user_booking = BookingModel.objects.filter(user = request.user)
    paginator = Paginator(user_booking, 5)
    page = request.GET.get('page', 1)

    try:
        user_bookings = paginator.page(page)
    except PageNotAnInteger:
        user_bookings = paginator.page(1)
    except EmptyPage:
        user_bookings = paginator.page(paginator.num_pages)


    if request.method == "POST":
        form = BookingForm(request.POST)

        if form.is_valid():
            form.save()
            messages.info(request, "Your booking request has been sent.")

        else:
            messages.error(
                "request", 'Something happened.. please try again later')

    form = BookingForm()
    return render(request, template_name='users/dashboard.html', context={"booking_form": form, 'bookings': user_bookings, 'user_bookings': user_booking})

@login_required(login_url="/login")
def profile_page_view(request):
    return render(request, 'users/profile.html')

def user_bookings_view(request):
    return render(request, 'users/booking.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You've successfully logged out of your account")
    return redirect("homepage")

