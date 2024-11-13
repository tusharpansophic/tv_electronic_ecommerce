from django.db import models

# Create your models here.
class Register(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    
class Category(models.Model):
    cat_name = models.CharField(max_length=50)
    def __str__(self):
        return self.cat_name

class Sub_category(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

# class Prod_Discount(models.Model):

class Product(models.Model):
    sub_category = models.ForeignKey(Sub_category, on_delete=models.CASCADE)
    pro_titel = models.CharField(max_length=50)
    pro_price = models.IntegerField()
    discounted_price = models.IntegerField()
    pro_description = models.CharField(max_length=100)
    pro_images = models.ImageField(upload_to="pro_images")

    def __str__(self):
        return self.pro_titel

    @property
    def discount_percentage(self):
        if self.pro_price > 0:  # Ensure original price is non-zero to avoid division by zero
            discount = ((self.pro_price - self.discounted_price) / self.pro_price) * 100
            disc = 100 - discount
            return round(disc, 2)  # Returns discount percentage rounded to two decimal places
        return 0

 
class Cart(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    total = models.IntegerField()
    qty = models.IntegerField()
    status = models.BooleanField(default=False)



class Address(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    mobile = models.IntegerField()
    landmark = models.CharField(max_length=100)
    city = models.CharField(max_length=100)


status_choices = [
("Pending","Pending"),
("PLACED","PLACED"),
("SHIPPED","SHIPPED"),
("DELIVERED","DELIVERED"),
]

class Order(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    product = models.CharField(max_length=500)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    order = models.CharField(max_length=50,choices=status_choices,default='Pending')

