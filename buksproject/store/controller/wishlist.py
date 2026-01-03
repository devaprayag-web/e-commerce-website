from django.shortcuts import render,redirect
from django.contrib import  messages
from store.form import CustomUserForm
from django.contrib.auth import authenticate,login,logout
from store.models import Product,Cart,Wishlist
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def index(request):
    print("LOGGED IN USER:", request.user, request.user.id)
    print("WISHLIST TABLE:", Wishlist.objects.values('id', 'user_id', 'product_id'))

    wishlist = Wishlist.objects.filter(user=request.user)
    print("USER WISHLIST:", wishlist)

    return render(request, "store/wishlist.html", {'wishlist': wishlist})



def addtowishlist(request):
    if request.method == "POST":

        if not request.user.is_authenticated:
            return JsonResponse({"status": "login to continue"})

        prod_id = request.POST.get('product_id')

        if not prod_id:
            return JsonResponse({"status": "invalid product id"})

        product = Product.objects.filter(id=prod_id).first()

        if not product:
            return JsonResponse({"status": "no such product found"})

        if Wishlist.objects.filter(user=request.user, product=product).exists():
            return JsonResponse({"status": "product already in wishlist"})

        Wishlist.objects.create(user=request.user, product=product)
        return JsonResponse({"status": "product added to wishlist"})

    return JsonResponse({"status": "invalid request"})

    

def removewishlistitem(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            prod_id = request.POST.get('product_id')
            wishlist_item = Wishlist.objects.filter(user=request.user, product_id=prod_id).first()
            if wishlist_item:
                wishlist_item.delete()
                return JsonResponse({"status": "removed"})
            else:
                return JsonResponse({"status": "not found"})
        else:
            return JsonResponse({"status": "login to continue"})
    return JsonResponse({"status": "invalid request"})



