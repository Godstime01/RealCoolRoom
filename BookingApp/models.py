from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self) -> str:
        return str(self.email)


class BookingModel(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    product_weight = models.DecimalField(decimal_places=3, max_digits=6, help_text="Enter weight of project in kg")
    status = models.BooleanField(default=False)
    due_date = models.DateTimeField()
    request_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField()

    def get_absolute_url(self):
        pass

    def calculate_price(self):
        if self.product_weight != None:
            return self.product_weight * 1000
        
        return 0

    def __str__(self) -> str:
        return f"{self.user} - request for {self.title}"
    