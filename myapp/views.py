from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Q
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
import random

# Create your views here.

# Helper for Email
def send_email_otp(email, otp):
    subject = 'Your Password Reset OTP'
    message = f'Your OTP for password reset is {otp}. Valid for 10 minutes.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)

# Authentication Views
def register(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        phone = request.POST['phone']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        user_exists = Register.objects.filter(email=email).exists()
        if user_exists:
            messages.error(request, 'Email already exists !!')
            return redirect('register')

        else:

            if pass1 == pass2:
                hashed_password = make_password(pass1)
                obj = Register(first_name=fname, last_name=lname,
                               email=email, phone=phone, pass1=hashed_password)
                obj.save()
                
                # Send Welcome Email
                try:
                    send_mail(
                        'Welcome to Organic Food Shop',
                        f'Hi {fname}, Thanks for registering with us.',
                        settings.EMAIL_HOST_USER,
                        [email],
                        fail_silently=True,
                    )
                except Exception as e:
                    print(e)
                    
                messages.success(request, 'You are Registered !!')
                return redirect('login')
            else:
                messages.error(request, 'Password are not match !!')
                return redirect('register')
    return render(request, "register.html")


def login(request):
    if request.method == "POST":
        email = request.POST['email']
        pass1 = request.POST['pass1']
        try:
            ob = Register.objects.get(email=email)
            password_ok = check_password(pass1, ob.pass1) or ob.pass1 == pass1
            if password_ok:
                messages.success(request, 'You are logged')
                request.session['user'] = email
                return redirect('myaccount')
            messages.error(request, ' Password Incorrect!!')
            return redirect('login')
        except Register.DoesNotExist:
            messages.error(request, 'User not Registered !!')
            return redirect('login')

    else:
        return render(request, "login.html")

# Forgot Password Views
def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = Register.objects.get(email=email)
            otp = str(random.randint(100000, 999999))
            user.otp = otp
            user.otp_created_at = timezone.now()
            user.save()
            
            send_email_otp(email, otp)
            request.session['reset_email'] = email
            messages.success(request, 'OTP sent to your email.')
            return redirect('verify_otp')
        except Register.DoesNotExist:
            messages.error(request, 'Email not found.')
            return redirect('forgot_password')
            
    return render(request, 'forgot_password.html')

def verify_otp(request):
    if request.method == "POST":
        otp = request.POST.get('otp')
        email = request.session.get('reset_email')
        
        if not email:
            return redirect('forgot_password')
            
        try:
            user = Register.objects.get(email=email)
            if user.otp == otp:
                # Check expiry (10 mins)
                if (timezone.now() - user.otp_created_at).total_seconds() < 600:
                    request.session['otp_verified'] = True
                    return redirect('reset_password')
                else:
                    messages.error(request, 'OTP expired.')
            else:
                messages.error(request, 'Invalid OTP.')
        except Register.DoesNotExist:
            return redirect('forgot_password')
            
    return render(request, 'verify_otp.html')

def reset_password(request):
    if not request.session.get('otp_verified'):
        return redirect('forgot_password')
        
    if request.method == "POST":
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        
        if pass1 == pass2:
            email = request.session.get('reset_email')
            user = Register.objects.get(email=email)
            hashed_password = make_password(pass1)
            user.pass1 = hashed_password
            user.otp = None
            user.save()
            
            del request.session['reset_email']
            del request.session['otp_verified']
            
            messages.success(request, 'Password reset successfully. Please login.')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')
            
    return render(request, 'reset_password.html')


# Profile & Account Views
def myaccount(request):
    if 'user' in request.session:
        email = request.session['user']
        user = Register.objects.get(email=email)
        my_orders = Order.objects.filter(user=user).order_by('-order_date')
        
        # Simple stats for premium dashboard cards
        total_orders = my_orders.count()
        pending_orders = my_orders.filter(order='Pending').count()
        placed_orders = my_orders.filter(order='PLACED').count()
        shipped_orders = my_orders.filter(order='SHIPPED').count()
        delivered_orders = my_orders.filter(order='DELIVERED').count()
        cancelled_orders = my_orders.filter(order='CANCELLED').count()
        
        total_spent = 0
        for o in my_orders:
            if o.total_amount:
                total_spent += float(o.total_amount)
        
        if request.method == "POST":
            user.first_name = request.POST.get('fname')
            user.last_name = request.POST.get('lname')
            
            new_pass = request.POST.get('pass1')
            if new_pass:
                hashed_password = make_password(new_pass)
                user.pass1 = hashed_password
                
            user.save()
            messages.success(request, 'Profile Updated Successfully')
            return redirect('myaccount')

        return render(
            request,
            "myaccount.html",
            {
                'user': user,
                'myorder': my_orders,
                'total_orders': total_orders,
                'pending_orders': pending_orders,
                'placed_orders': placed_orders,
                'shipped_orders': shipped_orders,
                'delivered_orders': delivered_orders,
                'cancelled_orders': cancelled_orders,
                'total_spent': round(total_spent, 2),
            },
        )
    return redirect('login')


def search(request):
    query = request.GET.get('q')
    if query:
        results = Product.objects.filter(product_name__icontains=query)
    else:
        results = Product.objects.all()
    return render(request, 'shop.html', {'prod': results})


def wishlist(request):
    if 'user' in request.session:
        email = request.session['user']
        user = Register.objects.get(email=email)
        wishlist_items = Wishlist.objects.filter(user=user)
        return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})
    return redirect('login')


def add_to_wishlist(request, id):
    if 'user' in request.session:
        email = request.session['user']
        user = Register.objects.get(email=email)
        product = Product.objects.get(id=id)
        
        if not Wishlist.objects.filter(user=user, product=product).exists():
            Wishlist.objects.create(user=user, product=product)
            messages.success(request, 'Added to Wishlist')
        else:
            messages.info(request, 'Item already in Wishlist')
            
        # Redirect back to the previous page
        return redirect(request.META.get('HTTP_REFERER', 'shop'))
    return redirect('login')


def remove_from_wishlist(request, id):
    if 'user' in request.session:
        Wishlist.objects.filter(id=id).delete()
        messages.success(request, 'Removed from Wishlist')
        return redirect('wishlist')
    return redirect('login')


# Cart Management Views
def plus(request, id):
    if 'user' not in request.session:
        return redirect('login')
    
    try:
        cart_item = Cart.objects.get(id=id, user__email=request.session['user'])
        product = cart_item.prod_name
        
        if cart_item.qty + 1 > product.stock:
            messages.error(request, f"Only {product.stock} items available!")
        else:
            cart_item.qty += 1
            cart_item.price = cart_item.qty * product.price
            cart_item.save()
    except Cart.DoesNotExist:
        messages.error(request, "Cart item not found")
        
    return redirect('cart')


def minus(request, id):
    if 'user' not in request.session:
        return redirect('login')
        
    try:
        cart_item = Cart.objects.get(id=id, user__email=request.session['user'])
        if cart_item.qty > 1:
            cart_item.qty -= 1
            cart_item.price = cart_item.qty * cart_item.prod_name.price
            cart_item.save()
        else:
            cart_item.delete()
    except Cart.DoesNotExist:
        messages.error(request, "Cart item not found")
        
    return redirect('cart')


def delete(request, id):
    if 'user' not in request.session:
        return redirect('login')
        
    Cart.objects.filter(id=id, user__email=request.session['user']).delete()
    return redirect('cart')


def cart(request):
    if 'user' not in request.session:
        return redirect("login")
    email = request.session['user']
    obj = Register.objects.get(email=email)
    obj1 = Cart.objects.filter(user_id=obj.id, status=False)
    list1 = []
    for i in obj1:
        list1.append(i.price)
    total = sum(list1)
    
    # Coupon Logic
    discount = 0
    final_total = total
    
    if request.method == "POST":
        if 'apply_coupon' in request.POST:
            code = request.POST.get('coupon_code')
            try:
                coupon = Coupon.objects.get(code=code, active=True)
                if coupon.valid_to >= timezone.now():
                    request.session['coupon_code'] = code
                    messages.success(request, 'Coupon applied successfully!')
                else:
                    messages.error(request, 'Coupon expired')
            except Coupon.DoesNotExist:
                messages.error(request, 'Invalid Coupon')
        elif 'remove_coupon' in request.POST:
             if 'coupon_code' in request.session:
                 del request.session['coupon_code']
                 messages.success(request, 'Coupon removed')
                 
    if 'coupon_code' in request.session:
        try:
            coupon = Coupon.objects.get(code=request.session['coupon_code'], active=True)
            if coupon.valid_to >= timezone.now():
                discount = (total * coupon.discount_percentage) / 100
                final_total = total - discount
            else:
                 del request.session['coupon_code']
        except:
             del request.session['coupon_code']

    return render(request, 'cart.html', {'cart_product': obj1, 'total': total, 'discount': discount, 'final_total': final_total})


def add_to_cart(request, id):
    if 'user' in request.session:
        user = Register.objects.get(email=request.session['user'])
        # Get product or redirect if not found
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            messages.error(request, 'Product not found.')
            return redirect('shop')

        # Stock check
        if product.stock <= 0:
            messages.error(request, 'This product is out of stock!')
            return redirect('shop')

        # Only consider current (not yet ordered) cart items
        cart_qs = Cart.objects.filter(
            user_id=user.id,
            prod_name_id=product.id,
            status=False
        )
        count = cart_qs.count()

        if count > 0:
            cart = cart_qs.first()
            # Do not allow quantity beyond available stock
            if cart.qty + 1 > product.stock:
                messages.error(request, f'Only {product.stock} items available!')
                return redirect('cart')
                
            qty = cart.qty + 1
            price = qty * product.price
            cart_qs.update(qty=qty, price=price)
            messages.success(request, 'Cart updated successfully.')
        else:
            # Create new cart item
            Cart.objects.create(
                user_id=user.id,
                prod_name_id=product.id,
                qty=1,
                price=product.price,
                status=False
            )
            messages.success(request, 'Product added to cart.')

        # After adding/updating, send user to cart page so they can see the item
        return redirect('cart')
    else:
        return redirect('login')


# logout
def logout(request):
    if 'user' in request.session:
        del request.session['user']
        if 'coupon_code' in request.session:
            del request.session['coupon_code']
        return redirect("index")
    return redirect('login')


# Product & Shop Views
def shop(request):
    """
    Shop page with optional category-based filtering plus sorting and price filters.
    Supported category values (via ?category=... in URL):
      - new     -> New Products
      - fruits  -> Fruit products
      - juice   -> Fruit Juice products
    """
    category = request.GET.get('category')

    # Base queryset according to category
    if category == 'new':
        prod = Product.objects.filter(cat_name__cat_name__icontains='New')
    elif category == 'fruits':
        prod = Product.objects.filter(cat_name__cat_name__icontains='Fruit').exclude(cat_name__cat_name__icontains='Juice')
    elif category == 'juice':
        prod = Product.objects.filter(cat_name__cat_name__icontains='Juice')
    else:
        prod = Product.objects.all()

    # Sorting and Filtering
    sort_by = request.GET.get('sort')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price:
        prod = prod.filter(price__gte=min_price)
    if max_price:
        prod = prod.filter(price__lte=max_price)

    if sort_by == 'price_low':
        prod = prod.order_by('price')
    elif sort_by == 'price_high':
        prod = prod.order_by('-price')
    elif sort_by == 'name_asc':
        prod = prod.order_by('product_name')

    return render(request, 'shop.html', {'prod': prod})


def indexView(request):
    # Fetch categories
    feaufruit = Product.objects.filter(cat_name__cat_name__icontains='Fruit').exclude(cat_name__cat_name__icontains='Juice')[:10]
    js = Product.objects.filter(cat_name__cat_name__icontains='Juice')[:10]
    new = Product.objects.filter(cat_name__cat_name__icontains='New')[:10]
    prod = Product.objects.all()

    context = {
        'feaufruit': feaufruit,
        'js': js,
        'new': new,
        'prod': prod,
    }
    return render(request, 'index.html', context)





def about(request):
    return render(request, 'about.html')


def feedback_view(request):
    user_data = None
    if request.session.get('user'):
        user_data = Register.objects.filter(email=request.session['user']).first()

    if request.method == "POST":
        if user_data:
            name = f"{user_data.first_name} {user_data.last_name}"
            email = user_data.email
            contact = user_data.phone or "N/A"
        else:
            name = request.POST.get('name')
            email = request.POST.get('email')
            contact = request.POST.get('contact')
            
        subject = request.POST.get('subject')
        comment = request.POST.get('comment')

        if name and email and subject and comment:
            ob = Feedback(name=name, email=email, contact=contact,
                          subject=subject, comment=comment)
            ob.save()
            messages.success(request, 'Feedback submitted successfully!')
            return redirect('feedback')
        else:
            messages.error(request, 'Please fill all required fields.')

    return render(request, 'contact.html', {'user_data': user_data})


def productdetails(request):
    sid = request.GET.get("cid")
    if sid is not None:
        sp = Product.objects.get(pk=sid)
        related_products = Product.objects.filter(cat_name=sp.cat_name).exclude(id=sp.id)[:4]
        return render(request, 'productdetails.html', {"pid": sp, "related_products": related_products})
    return redirect('shop')


def checkout(request):
    if 'user' in request.session:
        address_list = Address.objects.filter(
            user__email=request.session['user'])
        if request.method == "POST":

            user = Register.objects.get(email=request.session['user'])
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            address = request.POST['address']
            city = request.POST['city']
            state = request.POST['state']
            postcode = request.POST['postcode']
            email = request.POST['email']
            phone = request.POST['phone']

            obj = Address(user=user, first_name=first_name, last_name=last_name, address=address,
                          city=city, state=state, postcode=postcode, email=email, phone=phone)
            obj.save()
            messages.success(request, 'Address added successfully!')
            return redirect("checkout")
        email = request.session['user']
        obj = Register.objects.get(email=email)
        obj1 = Cart.objects.filter(user_id=obj.id, status=False)
        list1 = []
        for i in obj1:
            list1.append(i.price)
        total = sum(list1)
        
        # Apply Coupon
        discount = 0
        if 'coupon_code' in request.session:
             try:
                coupon = Coupon.objects.get(code=request.session['coupon_code'], active=True)
                if coupon.valid_to >= timezone.now():
                    discount = (total * coupon.discount_percentage) / 100
                else:
                    del request.session['coupon_code']
             except:
                del request.session['coupon_code']
                
        final_total = total - discount
        x = final_total + 50

        return render(request, 'checkout.html', {"address": address_list, "total": total, 'cart_product': obj1, "shipping": x, "discount": discount, "final_total": final_total})
    else:
        return redirect('login')


# Order & Checkout Views
def myorder(request):
    if 'user' in request.session:
        email = request.session['user']
        user = Register.objects.get(email=email)
        my_order = Order.objects.filter(user=user).order_by('-order_date')
        
        if request.method == "POST":
            address_id = request.POST.get("ADDRESS")
            payment_method = request.POST.get("payment_method", 'PAYTM')
            
            if not address_id:
                messages.error(request, "Please select an address")
                return redirect('checkout')

            try:
                address = Address.objects.get(pk=int(address_id))
            except Address.DoesNotExist:
                messages.error(request, "Invalid address")
                return redirect('checkout')

            obj1 = Cart.objects.filter(user=user, status=False)
            
            if not obj1.exists():
                 messages.warning(request, "Cart is empty")
                 return redirect('shop')

            # Check stock availability
            for item in obj1:
                if item.prod_name.stock < item.qty:
                    messages.error(request, f"Sorry, {item.prod_name.product_name} is out of stock (Available: {item.prod_name.stock})")
                    return redirect('cart')

            total = 0
            for item in obj1:
                total += item.price
            
            # Apply Coupon
            discount = 0
            if 'coupon_code' in request.session:
                 try:
                    coupon = Coupon.objects.get(code=request.session['coupon_code'], active=True)
                    if coupon.valid_to >= timezone.now():
                        discount = (total * coupon.discount_percentage) / 100
                    else:
                        del request.session['coupon_code']
                 except:
                    del request.session['coupon_code']
                    
            final_total = total - discount
            x = final_total + 50
            
            order = Order(
                user=user,
                address=address,
                payment_method=payment_method,
                total_amount=x,
            )
            order.save()

            # Deduct stock
            for item in obj1:
                item.prod_name.stock -= item.qty
                item.prod_name.save()

            # Mark cart items as ordered
            obj1.update(status=True)
            
            # Clear coupon
            if 'coupon_code' in request.session:
                del request.session['coupon_code']
                
            # Send Confirmation Email
            try:
                send_mail(
                    'Order Confirmation',
                    f'Hi {user.first_name}, Your order #{order.id} has been placed successfully. Total Amount: {x}',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=True,
                )
            except:
                pass

            if payment_method == 'COD':
                order.order = 'PLACED'
                order.save()
                messages.success(request, 'Order placed successfully! Payment will be collected on delivery.')
                return redirect('myorder')
            
            else:
                # Redirect to UPI Payment page
                return redirect('upi_payment', id=order.id)
        else:
            return render(request, 'myorder.html', {"myorder": my_order})
    else:
        return redirect('login')


def upi_payment(request, id):
    if 'user' in request.session:
        try:
            order = Order.objects.get(id=id, user__email=request.session['user'])
            
            # Generate UPI URL
            # format: upi://pay?pa=UPI_ID&pn=NAME&am=AMOUNT&tr=ORDER_ID&tn=NOTE
            upi_id = getattr(settings, 'UPI_MERCHANT_UPI_ID', 'paytmqr28100505010111432604778@paytm')
            merchant_name = getattr(settings, 'UPI_MERCHANT_NAME', 'Organic Food Shop')
            
            # Create QR Code Data
            # Note: In real app, you might generate a QR code image dynamically or use a static one
            # For this demo, we use a placeholder or a static image
            
            # Construct UPI Link for mobile apps
            amount = order.total_amount
            upi_url = f"upi://pay?pa={upi_id}&pn={merchant_name}&am={amount}&tr={order.id}&tn=Order_{order.id}"
            
            context = {
                'order': order,
                'total': amount,
                'upi_id': upi_id,
                'merchant_name': merchant_name,
                'upi_payment_url': upi_url
            }
            return render(request, 'upi_payment.html', context)
        except Order.DoesNotExist:
            messages.error(request, "Order not found")
            return redirect('myorder')
    return redirect('login')


def upi_payment_confirm(request, id):
    if 'user' in request.session:
        if request.method == "POST":
            try:
                order = Order.objects.get(id=id, user__email=request.session['user'])
                txn_id = request.POST.get('transaction_id')
                
                if txn_id:
                    order.upi_transaction_id = txn_id
                    order.payment_verified = False # Admin needs to verify
                    order.order = 'PLACED' # Temporarily placed, subject to verification
                    order.save()
                    
                    messages.success(request, f"Payment details submitted for Order #{order.id}. We will verify and process it shortly.")
                    return redirect('myorder')
                else:
                    messages.error(request, "Please enter Transaction ID")
                    return redirect('upi_payment', id=id)
                    
            except Order.DoesNotExist:
                messages.error(request, "Order not found")
                return redirect('myorder')
    return redirect('login')


def cancel_order(request, id):
    if 'user' in request.session:
        try:
            order = Order.objects.get(id=id, user__email=request.session['user'])
            
            if order.order == 'Pending' or order.order == 'PLACED':
                order.order = 'CANCELLED'
                order.save()
                messages.success(request, f"Order #{order.id} has been cancelled successfully.")
            else:
                messages.error(request, "Cannot cancel this order at this stage.")
                
        except Order.DoesNotExist:
            messages.error(request, "Order not found")
            
        return redirect('myaccount')
    return redirect('login')
