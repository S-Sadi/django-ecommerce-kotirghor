from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Item, Order, OrderItem
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

def cart_quantity_counter(req):
    total_quantity = 0
    if req.user.is_authenticated:
        try:
            u = Order.objects.get(user=req.user)
            item_list = u.items.filter(ordered=False)
            for i in item_list:
                total_quantity += i.quantity
        except Exception:
            #kotirghorapp.models.Order.DoesNotExist: Order matching query does not exist.
            #error handeling 
            pass
    return str(total_quantity)


def index(request):
    total_item= cart_quantity_counter(request)
    
    context = {
        "allitems": Item.objects.all(),
        "bitems": Item.objects.filter(category="BP"),
        "citems": Item.objects.filter(category="CP"),
        "eitems": Item.objects.filter(category="EP"),
        "total_quantity":total_item
    }
    return render(request, "index.html", context=context)

def product(request):
    total_item= cart_quantity_counter(request)
    context = {
        "allitems": Item.objects.all(),
        "bitems": Item.objects.filter(category="BP"),
        "citems": Item.objects.filter(category="CP"),
        "eitems": Item.objects.filter(category="EP"),
        "total_quantity":total_item
    }
    return render(request, "product.html", context=context)

@login_required(login_url="./login")
def payment(request):
    user_l = Order.objects.filter(user=request.user)
    if user_l.exists():
        u = user_l[0]
        cartlist = list(u.items.filter(ordered=False))
        total_price = 0
        for item in cartlist:
            total_price += item.get_total_price()
        if request.method == "POST":
            phone = request.POST.get("phonenum")
            txnid = request.POST.get("txnid", False)
            address = request.POST.get("address")
            if len(str(phone))>10 and len(address)>5:
                u.items.update(ordered=True)
                messages.success(request, "Payment successful")
                
            else:
                messages.error(request, "You payment unsuccessful please check all information")
            method = "CashOndelivery"
            if txnid:
                method = "Bkash"
            
            #send mail
        # mail_subject = "Kotirghor Payment Recive"
        # mail_message = "We are glade to inform you that, We recive your payment. You have purchase your product"
        # for item in cartlist:
        #     mail_message+"\n\t"+ str(item)
        
        # mail_message+"\n\nWe hope you have enjoy your purchases"
        # from_mail = settings.EMAIL_HOST_USER
        # to_mail = [request.user.email,]
        # send_mail(mail_subject, "Hello there", from_mail, to_mail, fail_silently=False)
        return render(request,"payment.html", context={"usercartlist":cartlist,"totalprice":total_price})
    else:
        return render(request, "payment.html")

def login(request):
    if request.method == "POST":
        e = request.POST["email"]
        p = request.POST["password"]
        try:
            USER_MODEL = get_user_model()
            user = USER_MODEL.objects.get(email=e)
        except USER_MODEL.DoesNotExist:
            messages.error(request, "Email doesn't exist")
            return redirect("./login")
        else:
            if user.password == p:
                auth.login(request,user)
                return redirect("./")
            else:
                messages.error(request, f"Invalid password: {user}")
    return render(request, "login.html")

def logout(request):
    auth.logout(request)
    return redirect("./")

def register(request):
    if request.method == "POST":
        user_name = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        repassword = request.POST["repassword"]
        
        if len(user_name)>3 and email.endswith((".com",".org",".net")) and len(password)>3:
            pass
        else:
            messages.error(request, "Please fill the form correctly")
            return render(request, "register.html")

        if password != repassword:
            messages.error(request, "Password incorrect")
            return render(request, "register.html")
        USER_MODEL = get_user_model()
        umail = USER_MODEL.objects.filter(email=email).exists()
        uname = USER_MODEL.objects.filter(username=user_name).exists()
        if uname:
            messages.error(request, "User Already exists (try:0-9)")
            return render(request, "register.html")
        if umail:
            messages.error(request, "User Already exists with this mail")
            return render(request, "register.html")
        else:
            user = USER_MODEL.objects.create(username=user_name, email=email, password=password)
            user.save()
            login(request)
        return redirect("./")
    else:
        return render(request, "register.html")

def about(request):
    return render(request, "about.html")
    
def contact(request):
    return render(request, "contact.html")

def privacy(request):
    return render(request, "Privacy and Policy.html")

def terms(request):
    return render(request, "Terms and Conditions.html")

def cart(request, slug):
    item_cart = get_object_or_404(Item, id=slug)
    total_item= cart_quantity_counter(request)
    context = {
        "item": item_cart,
        "total_quantity":total_item
    }
    if request.method == "POST":
            phone = request.POST.get("phonenum")
            txnid = request.POST.get("txnid", False)
            address = request.POST.get("address")
            if len(str(phone))>10 and len(address)>5:
                messages.success(request, "Payment successful")
                method = "CashOndelivery"
                if txnid:
                    method = "Bkash"
                u = Order.objects.get(user=request.user)                
                item, iscreated = OrderItem.objects.get_or_create(item=item_cart, user=request.user, ordered=True)
                if iscreated:
                    item.save()
                    u.items.add(item)
                else:
                    i = u.items.get(item__id=item_cart.id, ordered=True)
                    i.quantity+=1
                    i.save()
            else:
                messages.error(request, "You payment unsuccessful please check all information")
    return render(request, "cart.html", context=context)

def search_htm(request):
    total_item= cart_quantity_counter(request)
    if request.method == "POST":
        item_name = request.POST["searched"]
        searchitems = Item.objects.filter(title__icontains = item_name)
    else:
        searchitems = ""
    return render(request, "search.html", context={"searchitems": searchitems, "total_quantity":total_item})

@login_required(login_url="../login")
def addtocart(request, slug):
    item = get_object_or_404(Item, id=slug)
    items, iscreated = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    user = Order.objects.filter(user = request.user)
    if user.exists():
        if user[0].items.filter(item__id=item.id, ordered=False).exists():
            i = user[0].items.get(item__id=item.id, ordered=False)
            i.quantity +=1
            i.save()
        else:
            user[0].items.add(items)
    else:
        o = Order.objects.create(user = request.user)
        o.items.add(items)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
