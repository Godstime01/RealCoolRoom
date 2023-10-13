from django.urls import path
from . import views


urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("user/", views.user_dashboard, name='dashboard'),
    path("profile/", views.profile_page_view, name="user_profile"),
    path("bookings/", views.user_bookings_view, name='user_booking')
]
