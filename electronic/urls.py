"""electronic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [

 
    path('admin/', admin.site.urls),

    path('register/',views.register,name="register"),

    path('login/',views.login,name="login"),

    path("logout/",views.logout,name="logout"),


    
    path('',views.index,name="index"),
    
    path('checkout/',views.checkout,name="checkout"),

    path('minus/<int:id>',views.minus,name="minus"),

    path('plus/<int:id>',views.plus,name="plus"),

    path('remove/<int:id>',views.remove,name="remove"),

    
    path('contact/',views.contact,name="contact"),
    
    path('faqs/',views.faqs,name="faqs"),
    
    path('help/',views.help,name="help"),
    
    path('my_order/',views.my_order,name="my_order"),
    
    path('privacy/',views.privacy,name="privacy"),
    
    path('product/',views.product,name="product"),
    
    path('product2/',views.product2,name="product2"),
    
    path('single/',views.single,name="single"),
    
    path('single2/',views.single2,name="single2"),
    
    path('terms/',views.terms,name="terms"),

    path('about/',views.about,name="about"),

    path('add_to_cart/<int:id>',views.add_to_cart,name="add_to_cart"),

    path('address/',views.address,name="address"),

    path('initiate_payment/<int:total>/', views.initiate_payment, name='initiate_payment'),

    path('paymenthandler/', views.payment_handler, name='payment_handler'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
