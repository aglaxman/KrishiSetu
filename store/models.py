from django.db import models
from django.urls import reverse
from category.models import Category
# Create your models here.


class Product(models.Model):
    product_name    =models.CharField(max_length=200 , unique=True)
    slug            =models.SlugField(max_length=255 , unique=True)
    description     =models.TextField(max_length=500 , blank=True)
    price           =models.IntegerField()
    images          =models.ImageField(upload_to='photos/products')
    stock           =models.IntegerField()
    is_available    =models.BooleanField(default=True)
    category        =models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date    =models.DateTimeField(auto_now_add=True)
    modified_date   =models.DateTimeField(auto_now=True)


    def get_url(self):
        return reverse('product_detail',args=[self.category.slug , self.slug])

    def __str__(self):
        return self.product_name
    


from django.db import models
from django.utils import timezone
from django.utils.text import slugify

# ---------- Central User Table ----------
class User(models.Model):
    ROLE_CHOICES = [
        ('Farmer', 'Farmer'),
        ('Buyer', 'Buyer'),
        ('Agent', 'Agent'),
        ('Admin', 'Admin'),
        ('SuperAdmin', 'SuperAdmin')
    ]
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Suspended', 'Suspended')
    ]

    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    created_at = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.email

# ---------- Region ----------
class Region(models.Model):
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name}, {self.district}"

# ---------- Subscription Plan ----------
class SubscriptionPlan(models.Model):
    plan_name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField()
    features = models.TextField()

    def __str__(self):
        return self.plan_name

# ---------- Farmer ----------
class Farmer(models.Model):
    VERIFIED_CHOICES = [
        ('Pending','Pending'),
        ('Verified','Verified'),
        ('Rejected','Rejected')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    verified_status = models.CharField(max_length=20, choices=VERIFIED_CHOICES, default='Pending')
    assurance_tag = models.BooleanField(default=False)
    subscription = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

# ---------- Buyer ----------
class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    wishlist = models.ManyToManyField('Product', blank=True, related_name='wishlisted_by')

    def __str__(self):
        return self.name

# ---------- Agent ----------
class Agent(models.Model):
    STATUS_CHOICES = [('Active','Active'), ('Inactive','Inactive')]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    assigned_farmers = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')

    def __str__(self):
        return self.name

# ---------- Admin ----------
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

# ---------- SuperAdmin ----------
class SuperAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# ---------- Product ----------
# class Product(models.Model):
#     farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
#     category = models.CharField(max_length=100)
#     name = models.CharField(max_length=100)
#     slug = models.SlugField(max_length=255, unique=True, blank=True)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     stock_quantity = models.IntegerField()
#     assured = models.BooleanField(default=False)
#     image_url = models.URLField(blank=True)

#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.name)
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.name

# ---------- Lab Test Report ----------
class LabTestReport(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    test_date = models.DateTimeField(default=timezone.now)
    results = models.TextField()
    report_url = models.URLField()

# ---------- Order ----------
class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending','Pending'), ('Processing','Processing'),
        ('Delivered','Delivered'), ('Cancelled','Cancelled')
    ]
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

# ---------- Order Item ----------
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

# ---------- Payment ----------
class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [('UPI','UPI'),('Card','Card'),('NetBanking','NetBanking'),('Wallet','Wallet')]
    PAYMENT_STATUS_CHOICES = [('Pending','Pending'),('Completed','Completed'),('Failed','Failed'),('Refunded','Refunded')]
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES)
    payment_date = models.DateTimeField(default=timezone.now)

# ---------- Delivery Agent ----------
class DeliveryAgent(models.Model):
    STATUS_CHOICES = [('Available','Available'),('Busy','Busy'),('Inactive','Inactive')]
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Available')

# ---------- Delivery ----------
class Delivery(models.Model):
    DELIVERY_STATUS_CHOICES = [('Pending','Pending'),('Dispatched','Dispatched'),('Delivered','Delivered'),('Failed','Failed')]
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    delivery_agent = models.ForeignKey(DeliveryAgent, on_delete=models.SET_NULL, null=True)
    delivery_status = models.CharField(max_length=20, choices=DELIVERY_STATUS_CHOICES, default='Pending')
    estimated_date = models.DateField()
    actual_date = models.DateField(null=True, blank=True)
    tracking_number = models.CharField(max_length=100, blank=True)

# ---------- Review ----------
class Review(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

# ---------- Conflict Ticket ----------
class ConflictTicket(models.Model):
    STATUS_CHOICES = [('Open','Open'),('InProgress','InProgress'),('Resolved','Resolved'),('Escalated','Escalated')]
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True)
    admin = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, blank=True)
    superadmin = models.ForeignKey(SuperAdmin, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    description = models.TextField()
    resolution_note = models.TextField(blank=True)

# ---------- Notification ----------
class Notification(models.Model):
    TYPE_CHOICES = [('OrderUpdate','OrderUpdate'),('Payment','Payment'),('Subscription','Subscription'),('Conflict','Conflict'),('General','General')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    message = models.TextField()
    read_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

