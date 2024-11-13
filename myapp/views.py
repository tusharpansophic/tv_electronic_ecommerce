import razorpay
from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from .models import Register, Category, Sub_category, Product, Cart ,Address, Order
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


# Create your views here.
def register(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
        user_exist = Register.objects.filter(email=email).exists()
        if user_exist:
            messages.error(request,"Email Alredy exist!!")
            return redirect("/")
        else:
            if password == confirmpassword:
                obj = Register(name=name,email=email,password=password)
                obj.save()
                messages.success(request,"Refistration success fully !!!")
                return redirect("index")
            else:
                messages.error(request,"Password not match !!")
                return redirect("/")
    return redirect("register")

def login(request):
    messages.success(request,"Refistration success fully !!!")
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        try:
            valid = Register.objects.get(email=email)
            if valid.password == password:
                request.session['user']=email
                request.session['u_name']=valid.name
                return redirect("index")
            else:
                return redirect("login")
        except:
            return redirect("login")
    return redirect ("index")



def about(request):
    return render(request,"about.html")

def checkout(request):
    con={}
    if 'user' in request.session:
        user =  request.session['user']
        con['my_add'] = Address.objects.filter(user__email = user)

        con['cart']=Cart.objects.filter(user__email = user)
        cart =  Cart.objects.filter(user__email = user)

        total = 0
        qty = 0
        for c in cart:
            total += c.total
            qty += c.qty
        con['total']=total
        con['qty']=qty
        con['subtotal']=total
        return render(request,"checkout.html",con)
    else:
	    return redirect('login')

def address(request):
    if 'user' in request.session:
        user =  request.session['user']
        user = Address.objects.filter(user__email = user)
        if request.method == "POST":
            user = Register.objects.get(email=request.session['user'])
            name = request.POST['name']
            mobile = request.POST['mobile']
            landmark = request.POST['landmark']
            city = request.POST['city']
            obj = Address(user=user,name=name,mobile=mobile,landmark=landmark,city=city)
            obj.save()
            return redirect('checkout')
        return render(request,"address.html")
    else:
        return redirect("index")

def minus(request, id):
    # Fetch the cart item
    cart = get_object_or_404(Cart, id=id)
    total = cart.product.pro_price

    # Check if the quantity is greater than 1
    if cart.qty > 1:
        cart.qty -= 1
        cart.total = total * cart.qty
        cart.save()
    else:
        # If quantity is 1 or less, delete the cart item
        cart.delete()

    return redirect("checkout")


def plus(request,id):
    cart = Cart.objects.get(id=id)
    total = cart.product.pro_price
    cart.qty+=1
    cart.total = total*cart.qty
    cart.save()
    return redirect("checkout")

def remove(request,id):
    cart = Cart.objects.get(id=id)
    cart.delete()
    return redirect("checkout")


def contact(request):
    return render(request,"contact.html")

def faqs(request):
    return render(request,"faqs.html")

def help(request):
    return render(request,"help.html")

def index(request):
    mobile = Product.objects.filter(sub_category__category__cat_name = "electronics")
    appliances = Product.objects.filter(sub_category__category__cat_name="appliances")
    return render(request,"index.html",{"mobile":mobile,"app":appliances})


from django.shortcuts import render, redirect
from django.urls import reverse


def my_order(request):
    if 'user' in request.session:
        email = request.session['user']
        my_order = Order.objects.filter(user__email=email)
        my_add = Address.objects.filter(user__email=email)

        if request.method == "POST":
            address_id = request.POST.get("address")
            address = Address.objects.get(pk=int(address_id))
            user = Register.objects.get(email=email)
            cart_items = Cart.objects.filter(user__email=email)

            # Calculate total
            total = sum(item.product.pro_price for item in cart_items)# + 50
            cart_id_list = ",".join(str(item.id) for item in cart_items)

            # Store necessary order data as a dictionary in the session
            request.session['order_data'] = {
                'user_id': user.id,
                'address_id': address.id,
                'cart_id': cart_id_list,
                'total': total
            }
            # Redirect to initiate_payment with the total amount
            return redirect(reverse('initiate_payment', kwargs={'total': total}))
        return render(request, "my_order.html", {"my_order": my_order})

    return redirect("index")

def privacy(request): 
    return render(request,"privacy.html")

def product(request):
    con ={}
    con['product'] = Product.objects.filter(sub_category__category__cat_name = "electronics")
    if "cat" in request.GET:
        cat = request.GET.get("cat")
        con['product'] = Product.objects.filter(sub_category__name=cat)
    return render(request,"product.html",con)

def product2(request):
    con={}
    con['product'] = Product.objects.filter(sub_category__category__cat_name="appliances")
    if "cat" in request.GET:
        cat = request.GET.get("cat")
        con['product'] = Product.objects.filter(sub_category__name=cat)
    return render(request,"product2.html",con)

def single(request):
    # Get the product ID from the query parameter
    product_id = request.GET.get("cid")
    # If no product ID is provided, redirect to the home page (or another page)
    if product_id is None:
        return redirect("index")  # Replace "index" with your home page or appropriate page name
    # Retrieve the main product using the product ID
    sp = Product.objects.get(pk=product_id)
    related_products = Product.objects.all()[:12]

    # Render the single product page with the main product and related products
    return render(request, "single.html", {"sp": sp, "related_products": related_products})

def single2(request):
    return render(request,"single2.html")

def terms(request):
    return render(request,"terms.html")
                    
def logout(request):
    if 'user' in request.session:
        del request.session['user']
        return redirect("index")
    return redirect('login')
                     
def add_to_cart(request,id):
    con = {}
    if 'user' in request.session:
        user = request.session['user']
        us = Register.objects.get(email=user)
        product = Product.objects.get(pk=id)            
        cart_exists = Cart.objects.filter(user=us,product__pro_titel=product.pro_titel,status=False).exists()
        qty = 1
        if cart_exists:                  
            pass                           
        else:             
            Cart(user=us,product=product,qty=qty,total=product.pro_price).save()
            con['cart']= Cart.objects.filter(user__email = user)
    return redirect("index")

def initiate_payment(request, total):
    # Define payment details
    order_amount = total * 100  # amount in paise (e.g., 500.00 INR)
    order_currency = 'INR'
    order_receipt = 'order_rcptid_11'

    # Create Razorpay Order
    razorpay_order = razorpay_client.order.create({
        'amount': order_amount,
        'currency': order_currency,
        'receipt': order_receipt,
        'payment_capture': '1'  # Auto-capture payment
    })

    # Pass data to the template
    context = {
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_merchant_key': settings.RAZORPAY_KEY_ID,
        'amount': order_amount,
        'currency': order_currency,
        'callback_url': '/paymenthandler/'  # URL to handle payment response
    }
    return render(request, 'payment.html', context)


@csrf_exempt
def payment_handler(request):
    if request.method == 'POST':
        payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')

        try:
            # Verifying the payment signature
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result:
                # Retrieve order data from session
                order_data = request.session.get('order_data')

                if order_data:
                    # Retrieve necessary related objects
                    user = Register.objects.get(id=order_data['user_id'])
                    address = Address.objects.get(id=order_data['address_id'])
                    cart_id_list = order_data['cart_id']

                    # Save order in database
                    order = Order(
                        user=user,
                        # product=cart_id_list,
                        product=order_data['total'],
                        address=address,
                        # total_amount=order_data['total']
                    )
                    order.save()

                    # Clear cart items and session order data after saving order
                    Cart.objects.filter(id__in=[int(id) for id in cart_id_list.split(',')]).delete()
                    del request.session['order_data']

                    return redirect('my_order')  # Redirect to the order summary or success page

                else:
                    return JsonResponse({'status': 'Order data not found in session.'})
            else:
                return JsonResponse({'status': 'Payment verification failed.'})
        except Exception as e:
            return JsonResponse({'status': f'Error occurred: {str(e)}'})
