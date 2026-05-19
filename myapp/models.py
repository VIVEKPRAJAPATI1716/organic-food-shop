from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Register(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    pass1 = models.CharField(max_length=128)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Category(models.Model):
    cat_name = models.CharField(max_length=50)

    def __str__(self):
        return self.cat_name


class Product(models.Model):
    cat_name = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=50)
    price = models.IntegerField()
    description = models.CharField(max_length=1000)
    product_image = models.ImageField(upload_to="media/%y/%m/%d")
    stock = models.IntegerField(default=10)

    def __str__(self):
        return self.product_name


class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_percentage = models.IntegerField()
    valid_from = models.DateTimeField(default=timezone.now)
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} - {self.discount_percentage}%"


class Cart(models.Model):
    prod_name = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    qty = models.IntegerField()
    price = models.IntegerField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.prod_name.product_name


class Feedback(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    contact = models.CharField(max_length=15)
    subject = models.CharField(max_length=100)
    comment = models.TextField()

    def __str__(self):
        return self.name


class Address(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=70)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=40)
    postcode = models.CharField(max_length=10)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.first_name


status_choices = [
    ("Pending", "Pending"),
    ("PLACED", "PLACED"),
    ("SHIPPED", "SHIPPED"),
    ("DELIVERED", "DELIVERED"),
    ("CANCELLED", "CANCELLED"),
]


class Order(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    order = models.CharField(max_length=50, choices=status_choices, default='Pending')
    payment_method = models.CharField(max_length=20, default='UPI')
    payment_verified = models.BooleanField(default=False)
    upi_transaction_id = models.CharField(max_length=200, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class Wishlist(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.product_name
