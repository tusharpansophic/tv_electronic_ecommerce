from django.contrib import admin
from .models import Register, Category, Sub_category, Product ,Cart,Address, Order

# Register your models here.
# admin.site.register(Register),
admin.site.register(Category),
# admin.site.register(Sub_category),
# admin.site.register(Product),
# admin.site.register(Cart),
# admin.site.register(Address),
# admin.site.register(Order),

@admin.register(Sub_category)
class Sub_categoryAdmin(admin.ModelAdmin):
    list_display = ("id","category","name")


@admin.register(Register)
class RegisterAdmin(admin.ModelAdmin):
    list_display = ("id","name","email")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id","pro_titel","pro_price","discounted_price" ,"pro_description", "pro_images")

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("id","name","mobile","landmark" ,"city")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id","user","product","address","order_date" ,"order")

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'total', 'qty', 'status')
    list_filter = ('status', 'user')
    search_fields = ('user__username', 'product__name')
    ordering = ('-id',)
