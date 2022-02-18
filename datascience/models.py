from django.db import models
from registration.models import UserProfile
from django.utils import timezone
from .utils import generate_code
from django.shortcuts import reverse

class Customer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return str(self.name)


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name}"


class Position(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField(blank=True, null=True) # the price represents the result of "product" multiplied by "quantity"
    created = models.DateTimeField(blank=True, null=True) # blank=True, null=True in order to see them in Django admin
    
    def save(self, *args, **kwargs):
        self.price = self.product.price * self.quantity
        return super().save(*args, **kwargs)
    
    # We need the "sale id", however, we don't have any direct relation with the Sale table
    # We can get the sale id through the ManyToMany relationship filed on the Sale table -> reverse relationship
    def get_sales_id(self):
        sale_obj = self.sale_set.first() # .first() because in this project each position will belong to only one Sale object
        return sale_obj.id
    
    def __str__(self) -> str:
        return f"id: {self.id}, product: {self.product.name}, quantity: {self.quantity}"
    

class Sale(models.Model):
    transaction_id = models.CharField(max_length=12, blank=True) # we will create a function to generate it automaticly
    positions = models.ManyToManyField(Position) # the list of positions that we are including in the sale object
    total_price = models.FloatField(blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    salesman = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(blank=True, null=True) # blank=True, null=True in order to see them in Django admin
    updated = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if self.transaction_id == "": # we check to see if it's empty, because if not, we don't want to overwrite it
            self.transaction_id = generate_code()
        if self.created is None:
            self.created = timezone.now()
        return super().save(*args, **kwargs)

    # get all the positions related to the sale object by reffering to our ManyToMany field
    def get_positions(self): 
        return self.positions.all() # we will be able to loop through the positions
    
    # navigate to a particular page based on the app name, the name set in the path and the kwargs
    def get_absolute_url(self):
        return reverse("datascience:sale_details", kwargs={"pk": self.pk})
    
    def __str__(self) -> str:
        return f"Sales for the amount of {self.total_price}"


class CSV(models.Model):
    file_name = models.CharField(max_length=100, null=True, blank=True)
    csv_file = models.FileField(upload_to='csvs', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return str(self.file_name)


class Report(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to ="reports", blank=True, null=True)
    remarks = models.TextField()
    author = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.name)
    
    class Meta:
        ordering = ("-created",)

