from django.contrib import messages 
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from cart.models import Carts,CartItem, Paymentrazor
from store.models import Product
from .forms import Orderform
from .models import Order, Order_Product, Payment
from datetime import datetime
import datetime
from django.conf import settings
import razorpay
from accounts.models import Account, Profile, Wallet
from django.contrib.auth.decorators import login_required
import json
from django.views.decorators.csrf import csrf_exempt 
from django.conf import settings
from django.template.loader import render_to_string
#from weasyprint import HTML
import tempfile




# Create your views here.

def address(request):
    user = request.user
   
    if request.method == "POST":
      
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            Phone_number = request.POST['Phone_number']
            
            gender = request.POST['gender']
            house = request.POST['house']
            town = request.POST['town']
            locality = request.POST['locality']
            state = request.POST['state']
            country = request.POST['country']
            zip = request.POST['zip']
            pro=Profile.objects.create(user=user,first_name=first_name,last_name=last_name,Phone_number=Phone_number,gender=gender,house=house,town=town,locality= locality,state=state,country=country,zip=zip)
            pro.save()

            profile = Profile.objects.filter(user = user)
            
            return redirect('confirm_order')
         
    else:
        return render(request,'orders/address.html')




def confirm_order(request):
    user = request.user
    total = 0
    quantity = 0
    cart_items = CartItem.objects.filter(user=user)
    cart_count = cart_items.count()

    if (cart_count <= 0):
        return redirect('cart')
    for cart_item in cart_items:
        total += (cart_item.product.offer_price * cart_item.quantity)
        quantity += cart_item.quantity
    total = total + 40


    global val
    val = request.POST.get("address")

    if request.method == "POST": 
            profile = Profile.objects.get(user=user,id=val)
            cart_itm = Carts.objects.get(user = request.user)
            cart_itms = Carts.objects.filter(user = request.user)

            if cart_itm.final_offer_price > 0 :
                
                cart_i = cart_itm.final_offer_price  + 40
                cart_itms.update(final_offer_price = cart_i)
                total = cart_itm.final_offer_price
            else :
                cart_itms.update(final_offer_price = total)
            if Wallet.objects.filter(user = user).exists():
                wallet = Wallet.objects.get(user = request.user)
            else:
                wallet = "0"
            print(wallet)
            print("ivde")


            context = {
                       
                        'total' : total,
                        'val': val,
                        'cart_items' : cart_items,
                        'profile' : profile ,
                        'wallet' : wallet,
                    }
            return render(request,'orders/payment_select.html',context)
    else:
        
        profile = Profile.objects.filter(user = user)
        
        if Profile.objects.filter(user = user).exists():
            profile_avl = 1
        else:
            profile_avl = 0

       
        if Carts.objects.filter(user=request.user).exists():
            cart_item = Carts.objects.get(user=request.user)
            
            users=cart_item.user
            if cart_item.final_offer_price > 0 :
                total = cart_item.final_offer_price  + 40     
                
        context = {
            
            'total':total,
            'profile' : profile,
            'profile_avl' : profile_avl,
        }
        
        return render(request,'orders/place_order.html',context)

def place_order(request):
   
    user = request.user
   
    total = 0
    quantity = 0
   
    cart_items = CartItem.objects.filter(user=user)
    cart_count = cart_items.count()

    if (cart_count <= 0):
        return redirect('cart')
    for cart_item in cart_items:
        total += (cart_item.product.offer_price * cart_item.quantity)
        quantity += cart_item.quantity
    if request.method == "POST":              
        if Profile.objects.filter(id=val).exists():
            countt =1
            profile = Profile.objects.get(user=user,id=val)
            user = request.user
            first_name = profile.first_name
            last_name = profile.last_name
            phone_number = profile.Phone_number
            email = user.email
            town = profile.town
            house = profile.house
            country = profile.country
            state = profile.state
            zip = profile.zip
            order_total = total
            ip = request.META.get('REMOTE_ADDR')
            order=Order.objects.create(user=user,first_name=first_name,last_name=last_name,phone_number=phone_number,town=town,house=house,country=country,state=state,zip=zip,ip=ip, order_total = order_total, email=email)
            order.save()
            
            order_id_generated = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            order.order_number = order_id_generated

            order.save()
            order_id_generated = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            order.order_number = order_id_generated

            request.session['order_id'] = order.order_number

            order.save()

            order_id = order.order_number
         
            Order.objects.get(user=user,order_number=order_id)
            
            request.session['order_id'] = order.order_number
            context = {
                        'order_id' :order_id,
                        'total' : total,
                        'order':order,
                        'cart_items' : cart_items
                        
                    }
            
            
            return redirect('paypal_success')

        
    else:
        form = Orderform()
        profile = Profile.objects.filter(user = user)
        
        if Profile.objects.filter(user = user).exists():
            profile_avl = 1
        else:
            profile_avl = 0

        
        
        if Carts.objects.filter(user=request.user).exists():
            cart_item = Carts.objects.get(user=request.user)
            users=cart_item.user
            if cart_item.final_offer_price > 0 :
                total = cart_item.final_offer_price       

        context = {
            'form' : form,
            'total':total,
            'profile' : profile,
            'profile_avl' : profile_avl,
        }
        
        return render(request,'orders/place_order.html',context)

       
def payment_select(request,order_id):
    user = request.user
   
    order_id = request.session.get('order_id')
    
       
    orders = Order.objects.get( order_number = order_id)
    cart_items = CartItem.objects.filter(user=user)
    total = orders.order_total
    if Carts.objects.filter(user=request.user).exists():
            cart_item = Carts.objects.filter(user=request.user)
            users=cart_item.user
            if cart_item.final_offer_price > 0 :
                total = cart_item.final_offer_price + 40
            else :
                cart_item.update(final_offer_price = total + 40)
                
    

    context = {
            'cart_items':cart_items,
            'orders':orders,
            'total' : total,


        } 
        
    return render(request,'orders/payment_select.html',context)


def wallet_payment(request,val):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)
    carrt = Carts.objects.get(user=request.user)
    profile = Profile.objects.get(user=user,id=val)
  
    user = request.user
    first_name = profile.first_name
    last_name = profile.last_name
    phone_number = profile.Phone_number
    email = user.email
    town = profile.town
    house = profile.house
    country = profile.country
    state = profile.state
    zip = profile.zip
    order_total =  carrt.final_offer_price
    ip = request.META.get('REMOTE_ADDR')
    order=Order.objects.create(user=user,first_name=first_name,last_name=last_name,phone_number=phone_number,town=town,house=house,country=country,state=state,zip=zip,ip=ip, order_total = order_total, email=email)
    order.save()        
  
    order_id_generated = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
    order.order_number = order_id_generated
    order.save()
    order_id_generated = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
    order.order_number = order_id_generated

    request.session['order_id'] = order.order_number
    order.save()
    order_id = order.order_number          
    orders = Order.objects.get(user=user,order_number=order_id)
            
    request.session['order_id'] = order.order_number
     
    payment = Payment()
    payment.user = user
    payment.payment_id = order_id
    payment.payment_method = 'WALLET'
    payment.amount_paid=order.order_total
 
    payment.status = 'COMPLETED'
    payment.save()
    order.payment=payment
    order.is_ordered =True
    order.save()
    cart_itm = cart_items

    for item in cart_items:
        order_product = Order_Product()
        order_product.order = order
        order_product.payment = payment
        order_product.user = item.user
        order_product.product = item.product
        order_product.quantity =  item.quantity
        order_product.product_price = item.product.price
        order_product.ordered = True
        order_product.save()

        product =  Product.objects.get(id = item.product.id)
        product.stock = product.stock - item.quantity

        if product.stock <= 0:
            product.Is_available = False
        product.save()
        item.delete()
    order_product = Order_Product.objects.filter(user=user,payment = payment )

    total = order.order_total
    if Carts.objects.filter(user=request.user).exists():
            cart_item = Carts.objects.get(user=request.user)
            users=cart_item.user
            if cart_item.final_offer_price > 0 :
                total = cart_item.final_offer_price 
                ct = Carts.objects.filter(user=request.user)
                ct.update(final_offer_price=0)

    wallet = Wallet.objects.filter(user = user)
    wall = Wallet.objects.get(user = user)
    wallet_bal = wall.balance - total
    if wallet_bal >= 0 :
        wallet.update(balance = wallet_bal)
    else:
        wallet.update(balance = 0)
    
    context ={ 
        'order_product':order_product,
        'cart_itm':cart_itm,
        'order':order,
        'total': total,    
    }
    return render(request,'orders/invoice.html',context)

def cash_on_delivery(request,val):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)
    carrt = Carts.objects.get(user=request.user)
    profile = Profile.objects.get(user=user,id=val)
  
    user = request.user
    first_name = profile.first_name
    last_name = profile.last_name
    phone_number = profile.Phone_number
    email = user.email
    town = profile.town
    house = profile.house
    country = profile.country
    state = profile.state
    zip = profile.zip
    order_total =  carrt.final_offer_price
    ip = request.META.get('REMOTE_ADDR')
    order=Order.objects.create(user=user,first_name=first_name,last_name=last_name,phone_number=phone_number,town=town,house=house,country=country,state=state,zip=zip,ip=ip, order_total = order_total, email=email)
    order.save()        
  
    order_id_generated = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
    order.order_number = order_id_generated
    order.save()
    order_id_generated = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
    order.order_number = order_id_generated

    request.session['order_id'] = order.order_number
    order.save()
    order_id = order.order_number          
    orders = Order.objects.get(user=user,order_number=order_id)
            
    request.session['order_id'] = order.order_number
     
    payment = Payment()
    payment.user = user
    payment.payment_id = order_id
    payment.payment_method = 'COD'
    payment.amount_paid=order.order_total
 
    payment.status = 'Pending'
    payment.save()
    order.payment=payment
    order.is_ordered =True
    order.save()
    cart_itm = cart_items

    for item in cart_items:
        order_product = Order_Product()
        order_product.order = order
        order_product.payment = payment
        order_product.user = item.user
        order_product.product = item.product
        order_product.quantity =  item.quantity
        order_product.product_price = item.product.price
        order_product.ordered = True
        order_product.save()

        product =  Product.objects.get(id = item.product.id)
        product.stock = product.stock - item.quantity

        if product.stock <= 0:
            product.Is_available = False
        product.save()
        item.delete()
    order_product = Order_Product.objects.filter(user=user,payment = payment )

    total = order.order_total
    if Carts.objects.filter(user=request.user).exists():
            cart_item = Carts.objects.get(user=request.user)
            users=cart_item.user
            if cart_item.final_offer_price > 0 :
                total = cart_item.final_offer_price 
                ct = Carts.objects.filter(user=request.user)
                ct.update(final_offer_price=0)

    context ={ 
        'order_product':order_product,
        'cart_itm':cart_itm,
        'order':order,
        'total': total,    
    }
    return render(request,'orders/invoice.html',context)



def order_payment(request,check):
    request.session['check']  = check
    user =request.user

    user_o = Account.objects.get(id=user.id)
    
    request.session['user']  = user_o.id
    cart = Carts.objects.get(user=request.user)
    amount = cart.final_offer_price
        
        
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    razorpay_order = client.order.create(
            {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
        )

    payment = Paymentrazor.objects.create(
            user=user_o, total_amount=amount, order_id=razorpay_order['id']
        )
    payment.save()
    return render(
            request,
            "orders/razorpayment.html",
            {
                "callback_url": "https://" + "www.ajaykj.live" + "/orders/razorpay/callback/",
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "order": payment,
            },
        )
  
@csrf_exempt
def callback(request):
    
    if  request.method == 'POST':
        
        payment_id = request.POST.get("razorpay_payment_id", "")
        
        provider_order_id = request.POST.get("razorpay_order_id", "")
       
        signature_id = request.POST.get("razorpay_signature", "")
        try:
            order = Paymentrazor.objects.get(order_id=provider_order_id)
        except:
            
            provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id")
           
            order = Paymentrazor.objects.get(order_id=provider_order_id)

            return render(request, "orders/callback.html", context={"status": "FAILED"})


        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        result = client.utility.verify_payment_signature({
        'razorpay_order_id': provider_order_id,
        'razorpay_payment_id': payment_id,
        'razorpay_signature': signature_id
        })

        order.payment_id = payment_id
        order.signature_id = signature_id    
        order.save()
        if result:
        
            order.status = 'Confirmed'
            order.save()
            
            return redirect(course_changer)
        else:
            order.status = 'FAILED'
            order.save()

            return render(request, "orders/callback.html", context={"status": order.status})
    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = 'FAILED'
        order.save()
        return render(request, "orders/callback.html", context={"status": order.status})
    
def course_changer(request):
    check = request.session.get('check')
  
    return redirect(razorpay_success)



def razorpay_success(request):
    user = request.user

    total = 0
    quantity = 0
   
    cart_items = CartItem.objects.filter(user=user)
    cart_count = cart_items.count()

    if (cart_count <= 0):

        return redirect('cart')
    for cart_item in cart_items:
        total += (cart_item.product.offer_price * cart_item.quantity)
        quantity += cart_item.quantity
   
    if Profile.objects.filter( id = val ).exists():
            countt =1
            profile = Profile.objects.get(user=user,id=val)

            user = request.user
            first_name = profile.first_name
            last_name = profile.last_name
            phone_number = profile.Phone_number
            email = user.email
            town = profile.town
            house = profile.house
            country = profile.country
            state = profile.state
            zip = profile.zip
            order_total = total
            ip = request.META.get('REMOTE_ADDR')
            order=Order.objects.create(user=user,first_name=first_name,last_name=last_name,phone_number=phone_number,town=town,house=house,country=country,state=state,zip=zip,ip=ip, order_total = order_total, email=email)
            order.save()
            
            order_id_generated = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            order.order_number = order_id_generated

            order.save()
            order_id_generated = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            order.order_number = order_id_generated

            request.session['order_id'] = order.order_number

            order.save()

            order_id = order.order_number
           
            Order.objects.get(user=user,order_number=order_id)
            
            request.session['order_id'] = order.order_number
    
            order_id = request.session.get('order_id')
 
            order = Order.objects.get(order_number = order_id)
            cart_items = CartItem.objects.filter(user=user)
        
            payment = Payment()
            payment.user = user
            payment.payment_id = order_id
            payment.payment_method = 'RAZORPAY'
            payment.amount_paid=order.order_total
            payment.status = 'COMPLETED'
            payment.save()
            order.payment=payment
            order.is_ordered =True
            order.save()
            for item in cart_items:
                order_product = Order_Product()
                order_product.order = order
                order_product.payment = payment
                order_product.user = item.user
                order_product.product = item.product
                order_product.quantity =  item.quantity
                order_product.product_price = item.product.price
                order_product.ordered = True
                order_product.save()

                product =  Product.objects.get(id = item.product.id)
                product.stock = product.stock - item.quantity

                if product.stock <=0:
                    product.Is_available = False
                product.save()
        
                return redirect(payment_successfull)


def paypal_success(request):
    user = request.user
    order_id = request.session.get('order_id')
 
    order = Order.objects.get(order_number = order_id)
    cart_items = CartItem.objects.filter(user=user)
        
    payment = Payment()
    payment.user = user
    payment.payment_id = order_id
    payment.payment_method = 'PAYPAL'
    payment.amount_paid=order.order_total
    payment.status = 'COMPLETED'
    payment.save()
    order.payment=payment
    order.is_ordered =True
    order.save()
    for item in cart_items:
        order_product = Order_Product()
        order_product.order = order
        order_product.payment = payment
        order_product.user = item.user
        order_product.product = item.product
        order_product.quantity =  item.quantity
        order_product.product_price = item.product.price
        order_product.ordered = True
        order_product.save()

        product =  Product.objects.get(id = item.product.id)
        product.stock = product.stock - item.quantity

        if product.stock <=0:
            product.Is_available = False
        product.save()
        
    return JsonResponse({'completed':'success'})


   

def payment_successfull(request):
    cart_item = CartItem.objects.filter(user=request.user)
    order_id = request.session.get('order_id')
    

    order = Order.objects.get(order_number = order_id)
    order_product = Order_Product.objects.filter(user=request.user , payment = order.payment)

    cart_itm = cart_item
   
    cart_item.delete()
    total = order.order_total
    if Carts.objects.filter(user=request.user).exists():
            cart_item = Carts.objects.get(user=request.user)
            users=cart_item.user
            if cart_item.final_offer_price > 0 :
                total = cart_item.final_offer_price 
                ct = Carts.objects.filter(user=request.user)
                ct.update(final_offer_price=0)
    print(order_product)
    print("000")
    context ={ 
        'order_product':order_product,
        'cart_itm':cart_itm,
        'order':order,
        'total':total
    }
  
    return render(request,'orders/invoice.html',context)


@login_required()
def my_orders(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    order_items = Order_Product.objects.filter(user=user)
    context = {
        'orders' : orders,
        'order_items':order_items
    }
    return render(request,'orders/my_orders.html',context)


def order_view(request,id):
    user =  request.user
    if Order.objects.filter(id=id).exists():
        orders = Order.objects.get(id=id )
        order_items = Order_Product.objects.filter(order_id=id)
        
        context ={
            'order_items':order_items,
            'orders':orders
        }

        return render(request,'orders/order_view_list.html',context)
    else :
        messages.success(request,'no order found')
        return redirect('my_orders')


def order_cancel(request,id):
    user = request.user
    orders = Order.objects.get(id=id,user=user)
    paymnt = orders.payment.payment_method

    if paymnt == 'COD' : 
        orders.status = 'Cancelled'
        orders.save()
    elif paymnt == 'PAYPAL' or paymnt == 'RAZORPAY' : 
        if Wallet.objects.filter(user = user).exists:
            wallet = Wallet.objects.get(user = user)
            bal = wallet.balance + orders.order_total
            wallt = Wallet.objects.filter(user = user)
            wallt.update(balance = bal)
            orders.status = 'Cancelled'
            orders.save()
        else:
            wallet = Wallet.objects.create(
                user = user,
                balance = orders.order_total
                )
            
            wallet.save()
            orders.status = 'Cancelled'
            orders.save()

    return redirect('my_orders')

def order_return(request,id):

    user = request.user
    orders = Order.objects.get(id=id,user=user)
 
    if Wallet.objects.filter(user = user).exists:
        wallet = Wallet.objects.get(user = user)
        bal = wallet.balance + orders.order_total
        wallt = Wallet.objects.filter(user = user)
        wallt.update(balance = bal)
        orders.status = 'Returned'
        orders.save()
    else:
        wallet = Wallet.objects.create(
            user = user,
            balance = orders.order_total
            )
            
        wallet.save()
        orders.status = 'Returned'
        orders.save()

    return redirect('order_view',id)


def export_invoice_pdf(request):
    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition'] = 'inline; attachement; filename=Invoice' +'.pdf'

    response['Content-Transfer-Encoding'] = 'binary'

    order_product = Order_Product.objects.filter(user=request.user)
    cart_item = CartItem.objects.filter(user=request.user)
    order_id = request.session.get('order_id')

    cart_itm = cart_item
    order = Order.objects.get(order_number = order_id)

    cart_item.delete()
    total = order.order_total
    if Carts.objects.filter(user=request.user).exists():
            cart_item = Carts.objects.get(user=request.user)
            users=cart_item.user
            if cart_item.final_offer_price > 0 :
                total = cart_item.final_offer_price 
                ct = Carts.objects.filter(user=request.user)
                c = ct.update(final_offer_price=0)
    context ={ 
        'order_product':order_product,
        'cart_itm':cart_itm,
        'order':order,
        'total':total
    }

    html_string = render_to_string('orders/pdf_output_invoice.html',context)

    #html=HTML(string=html_string)

    #result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output : 
        #output.write(result)
        output.flush()


        output=open(output.name,'rb')

        response.write(output.read())

    return response


