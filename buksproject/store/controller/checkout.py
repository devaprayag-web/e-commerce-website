from django.shortcuts import render,redirect
from django.contrib import  messages
from store.form import CustomUserForm
from django.contrib.auth import authenticate,login,logout
from store.models import Product,Cart,Wishlist,Profile, Order, OrderItem
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    cart = Cart.objects.filter(user=request.user)

    total_price = sum(
        item.product.selling_price * item.product_qty for item in cart
    )

    context = {
        'cart': cart,
        'total_price': total_price
    }
    return render(request, "store/checkout.html", context)

def placeorder(request):
    if request.method == "POST":
        currentuser = request.user

        currentuser.first_name = request.POST.get('firstname', '')
        currentuser.last_name = request.POST.get('lastname', '')
        currentuser.save()

        # Profile
        if not Profile.objects.filter(user=currentuser).exists():
            userprofile = Profile()
            userprofile.user = currentuser
            userprofile.phone = request.POST.get('phone', '')
            userprofile.address = request.POST.get('address', '')
            userprofile.city = request.POST.get('city', '')
            userprofile.state = request.POST.get('state', '')
            userprofile.country = request.POST.get('country', '')
            userprofile.pincode = request.POST.get('pincode', '')
            userprofile.save()

        neworder = Order(
            user=currentuser,
            fname=currentuser.first_name,
            lname=currentuser.last_name,
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),          # ✅ FIXED
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            country=request.POST.get('country'),
            pincode=request.POST.get('pincode'),
            payment_mode=request.POST.get('payment_mode'),
            payment_id=request.POST.get('payment_mode'),
        )

        cart = Cart.objects.filter(user=currentuser)
        neworder.total_price = sum(
            item.product.selling_price * item.product_qty for item in cart
        )

        import random
        trackno = 'Amritha' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_no=trackno).exists():
            trackno = 'Amritha' + str(random.randint(1111111, 9999999))

        neworder.tracking_no = trackno
        neworder.save()

        for item in cart:
            OrderItem.objects.create(
                order=neworder,
                product=item.product,
                price=item.product.selling_price,
                quantity=item.product_qty
            )

            item.product.quantity -= item.product_qty
            item.product.save()

        cart.delete()

        messages.success(request, "Your order has been placed successfully")

        if request.POST.get('payment_mode') == "paid by razorpay":
            return JsonResponse({"status": "Order placed successfully"})

    return redirect('order')


def razorpaycheck(request):
        cart = Cart.objects.filter(user=request.user)
        total_price = 0
        for item in cart:
            total_price += item.product.selling_price * item.product_qty
        return JsonResponse({
            'total_price':total_price
        })    
