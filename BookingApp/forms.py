from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import CustomUser, BookingModel



class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", 'password2')



class BookingForm(forms.ModelForm):
    class Meta:
        model = BookingModel
        fields = "__all__"