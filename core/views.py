from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from django.db.models import Q,F
from .forms import CheckoutForm, CouponForm, RefundForm
from .models import Item, OrderItem, Order, BillingAddress, Payment, Coupon, Refund, Category
from track.models import Product_Track
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.shortcuts import render_to_response
from django.utils import timezone
from track.models import UserProfile
#from cassandra.cluster import Cluster
# Create your views here.
import random
import string
import requests
import stripe
import json
import itertools
import datetime
import time
stripe.api_key = settings.STRIPE_SECRET_KEY

def get_cartid(userid):
    now = datetime.datetime.now()
    current_time = now.strftime("%H%M")
    date = datetime.datetime.now().strftime('%d%m%y')
    j=0;
    while(j<=2400):
        if (j>int(current_time)):
            return(str(userid)+str(date)+str(j))
        elif (j==2400):
            return(str(userid)+str(date)+'2400')
        j=j+1200
#http://af787bc2a7bfa42e38ed91dc51fcbab9-980046495.ap-southeast-1.elb.amazonaws.com:5000/getcart_touch_points
def product_tracking(request):
    event = request.GET.get('event')
    url = 'http://af787bc2a7bfa42e38ed91dc51fcbab9-980046495.ap-southeast-1.elb.amazonaws.com:5000/getcart_touch_points'

    if event.lower() == 'product_viewed':

        user_id = request.GET.get("user_id")
        user_email = request.GET.get("user_email")
        product_name = request.GET.get("product_name")
        check_product = Product_Track.objects.all().filter(~Q(event='order_confirmed'),user_id=user_id,product_name=product_name,user_status='active')
        if not check_product:
            product = Product_Track()
            product.user_id = user_id
            product.user_email = user_email
            product.product_name = product_name
            product.product_price = float(request.GET.get("selling_price"))
            product.product_category = request.GET.get("product_category")
            product.sku_id = request.GET.get("sku_id")
            product.event = 'product_viewed'
            product.product_view_count = 1
            product.merchant_id = int(request.GET.get("merchant_id"))
            product.mob_no = int(request.GET.get("user_mobile_number"))
            product.save()
            #cluster = Cluster()
            #session = cluster.connect("aneja_keyspace")
            #rows = session.execute("INSERT INTO product_track (ptrack_id,user_id,user_email,product_name,product_category,product_price,sku_id,event) VALUES ('{}', '{}', '{}', '{}', '{}', {}, '{}', 'product_viewed')".format(str(product.ptrack_id), product.user_id, product.user_email, product.product_name, product.product_category, int(product.product_price), product.sku_id))

        else:
            check_product.update(product_view_count = F('product_view_count')+1)
            check_product.update(timestamp = datetime.datetime.now())
        myobj = {
            "merchant_id": int(request.GET.get("merchant_id")),
            "accountType": request.GET.get("accountType"),
            "user_id": request.GET.get("user_id"),
            "cart_id": get_cartid(request.GET.get("user_id")),
            "quantity": int(request.GET.get("quantity")),
            "product_category": request.GET.get("product_category"),
            "product_name": request.GET.get("product_name"),
            "selling_price": float(request.GET.get("selling_price")),
            "user_mobile_number": str(request.GET.get("user_mobile_number")),
            "sku_id":  request.GET.get("sku_id"),
            "user_email":  request.GET.get("user_email"),
            "event": 'product_viewed',
            "ordertype": "Normal_Order",
            "user_status": "active",
            "product_view_count": 1
        }
        req = requests.post(url, json = myobj)
        print(req.text)
    elif event.lower() == 'add_to_cart':

        user_id = request.GET.get("user_id")
        product = Product_Track.objects.all().filter(event='product_viewed',user_id=user_id,user_status='active').order_by('-timestamp').first()#.update(event='add_to_cart')
        #print(product)
        if  product:

            cart = Product_Track.objects.all().filter(counter=product.counter)
            #print(cart)
            cart.update(cartid = get_cartid(user_id))
            cart.update(timestamp = datetime.datetime.now())
            cart.update(event='add_to_cart')
            cart.update(product_unit = int(request.GET.get("quantity")))
            cart.update(order_total = float(request.GET.get("order_total")))
            myobj = {
                "merchant_id": int(request.GET.get("merchant_id")),
                "accountType": request.GET.get("accountType"),
                "user_id": request.GET.get("user_id"),
                "cart_id": get_cartid(request.GET.get("user_id")),
                "quantity": int(request.GET.get("quantity")),
                "product_category": product.product_category,
                "product_name": product.product_name,
                "selling_price": float(product.product_price),
                "user_mobile_number": str(request.GET.get("user_mobile_number")),
                "sku_id":  product.sku_id,
                "user_email":  request.GET.get("user_email"),
                "event": 'add_to_cart',
                "ordertype": "Normal_Order",
                "user_status": "active",
                "product_view_count": 1
            }
            req = requests.post(url, json = myobj)
            print(req.text)
            #Product_Track.objects.filter(~Q(event='order_confirmed'),user_id=user_id,user_status='active').order_by('-timestamp').update(cartid=get_cartid(user_id),event='add_to_cart').first()
            #Product_Track.objects.filter(~Q(event='order_confirmed'),user_id=user_id,user_status='active').order_by('-timestamp').first()
        else:
            myobj = {
                "merchant_id": int(request.GET.get("merchant_id")),
                "accountType": request.GET.get("accountType"),
                "user_id": request.GET.get("user_id"),
                "cart_id": get_cartid(request.GET.get("user_id")),
                "user_mobile_number": str(request.GET.get("user_mobile_number")),
                "quantity": int(request.GET.get("quantity")),
                "user_email":  request.GET.get("user_email"),
                "event": 'add_to_cart',
                "ordertype": "Normal_Order",
                "user_status": "active",
                "product_view_count": 1
            }
            req = requests.post(url, json = myobj)
            print(req.text)
    elif event.lower() == 'checkout_initiated':
        user_id = request.GET.get("user_id")
        product = Product_Track.objects.all().filter(~Q(event='order_confirmed'),user_id=user_id,user_status='active').order_by('-timestamp')#.update(event='add_to_cart')
        cart = Product_Track.objects.all().filter(cartid=product[0].cartid)
        #print(cart)
        cart.update(timestamp = datetime.datetime.now())
        cart.update(product_unit = int(request.GET.get("quantity")))
        cart.update(order_total = float(request.GET.get("order_total")))
        cart.update(event='checkout_initiated')
        myobj = {
            "merchant_id": int(request.GET.get("merchant_id")),
            "accountType": request.GET.get("accountType"),
            "user_id": request.GET.get("user_id"),
            "cart_id": get_cartid(request.GET.get("user_id")),
            "user_mobile_number": str(request.GET.get("user_mobile_number")),
            "quantity": int(request.GET.get("quantity")),
            "user_email":  request.GET.get("user_email"),
            "event": 'checkout_initiated',
            "ordertype": "Normal_Order",
            "user_status": "active",
            "product_view_count": 1
        }
        req = requests.post(url, json = myobj)
        print(req.text)
    elif event.lower() == 'order_confirmed':
        user_id = request.GET.get("user_id")
        product = Product_Track.objects.all().filter(~Q(event='order_confirmed'),user_id=user_id,user_status='active').order_by('-timestamp')#.update(event='add_to_cart')
        cart = Product_Track.objects.all().filter(cartid=product[0].cartid)
        #print(cart)
        myobj = {
            "merchant_id": int(request.GET.get("merchant_id")),
            "accountType": request.GET.get("accountType"),
            "user_id": request.GET.get("user_id"),
            "cart_id": get_cartid(request.GET.get("user_id")),
            "user_mobile_number": str(request.GET.get("user_mobile_number")),
            "quantity": int(request.GET.get("quantity")),
            "user_email":  request.GET.get("user_email"),
            "event": 'order_confirmed',
            "ordertype": "Normal_Order",
            "user_status": "active",
            "product_view_count": 1
        }
        req = requests.post(url, json = myobj)
        print(req.text)
        cart.update(timestamp = datetime.datetime.now())
        cart.update(user_status = 'order_completed')
        cart.update(order_total = float(request.GET.get("order_total")))
        cart.update(event='order_confirmed')

    else:
        print('hello')


    return HttpResponse(status=201)



def get_cart(self, *args, **kwargs):
    try:

        order = Order.objects.get(user=self.request.user, ordered=False)
        return(order)

    except ObjectDoesNotExist:

        messages.error(self.request, "You do not have an active order")
        return 1

def current_user(request):
    current_user = request.user
    return current_user

def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


class PaymentView(View):
    def get(self, *args, **kwargs):
        # order
        order = Order.objects.get(user=self.request.user, ordered=False)
        mobile = UserProfile.objects.get(user=self.request.user)
        if order.billing_address:
            context = {
                'order': order,
                'DISPLAY_COUPON_FORM': False,
                'mobile': mobile.mobile
            }
            return render(self.request, "payment.html", context)
        else:
            messages.warning(
                self.request, "u have not added a billing address")
            return redirect("core:checkout")

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        amount = int(order.get_total())
        #try:

        # create the payment
        payment = Payment()
        payment.stripe_charge_id = create_ref_code()
        payment.user = self.request.user
        payment.amount = order.get_total()
        payment.save()

        # assign the payment to the order
        order.ordered = True
        order.payment = payment
        # TODO : assign ref code
        order.ref_code = create_ref_code()
        order.save()

        messages.success(self.request, "Order was successful")
        return redirect("/")



class HomeView(View):

    def get(self, *args, **kwargs):

        if self.request.user.is_authenticated:

            order_exist = Order.objects.filter(user=self.request.user, ordered=False)

            if order_exist:
                order = Order.objects.get(user=self.request.user, ordered=False)

                items = Item.objects.filter(is_active=True)
                context = {
                    'object': order,
                    'items' : items
                }

                return render(self.request, 'index.html', context)

            else:
                items = Item.objects.filter(is_active=True)
                context = {
                    'items' : items
                }
                return render(self.request, 'index.html', context)
        else:
            items = Item.objects.filter(is_active=True)
            context = {
                'items' : items
            }
            return render(self.request, 'index.html', context)


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            mobile = UserProfile.objects.get(user=self.request.user)

            context = {
                'object': order,
                'mobile': mobile.mobile
            }
            print(context)
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")




class ShopView(ListView):
    model = Item
    paginate_by = 6
    template_name = "shop.html"
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        if self.request.user.is_authenticated:
            order_exist = Order.objects.filter(user=self.request.user, ordered=False)
            if  order_exist:

                context['object'] = Order.objects.get(user=self.request.user, ordered=False)

        return context


class ItemDetailView(DetailView):
    model = Item
    template_name = "product-detail.html"
    def get_context_data(self, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        if not self.request.user.is_anonymous:
            mobile = UserProfile.objects.get(user=self.request.user)
            context['Mobile'] = mobile.mobile
        return context

# class CategoryView(DetailView):
#     model = Category
#     template_name = "category.html"

class CategoryView(View):
    def get(self, *args, **kwargs):

        if self.request.user.is_authenticated:

            order_exist = Order.objects.filter(user=self.request.user, ordered=False)

            if order_exist:

                order = Order.objects.get(user=self.request.user, ordered=False)
                category = Category.objects.get(slug=self.kwargs['slug'])
                item = Item.objects.filter(category=category, is_active=True)

                context = {
                    'object': order,
                    'object_list': item,
                    'category_title': category,
                    'category_description': category.description,
                    'category_image': category.image
                }
                return render(self.request, "category.html", context)

            else:
                category = Category.objects.get(slug=self.kwargs['slug'])
                item = Item.objects.filter(category=category, is_active=True)

                context = {

                    'object_list': item,
                    'category_title': category,
                    'category_description': category.description,
                    'category_image': category.image
                }
                return render(self.request, "category.html", context)

        else:
            category = Category.objects.get(slug=self.kwargs['slug'])
            item = Item.objects.filter(category=category, is_active=True)

            context = {

                'object_list': item,
                'category_title': category,
                'category_description': category.description,
                'category_image': category.image
            }
            return render(self.request, "category.html", context)



class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            mobile = UserProfile.objects.get(user=self.request.user)
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True,
                'mobile': mobile.mobile
            }
            return render(self.request, "checkout.html", context)

        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("core:checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            print(self.request.POST)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                # add functionality for these fields
                # same_shipping_address = form.cleaned_data.get(
                #     'same_shipping_address')
                # save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip=zip,
                    address_type='B'
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()

                # add redirect to the selected payment option
                if payment_option == 'S':
                    return redirect('core:payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('core:payment', payment_option='paypal')
                else:
                    messages.warning(
                        self.request, "Invalid payment option select")
                    return redirect('core:checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("core:order-summary")


# def home(request):
#     context = {
#         'items': Item.objects.all()
#     }
#     return render(request, "index.html", context)
#
#
# def products(request):
#     context = {
#         'items': Item.objects.all()
#     }
#     return render(request, "product-detail.html", context)
#
#
# def shop(request):
#     context = {
#         'items': Item.objects.all()
#     }
#     return render(request, "shop.html", context)


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Item qty was updated.")
            return redirect("core:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "Item was added to your cart.")
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item was added to your cart.")
    return redirect("core:order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "Item was removed from your cart.")
            return redirect("core:order-summary")
        else:
            # add a message saying the user dosent have an order
            messages.info(request, "Item was not in your cart.")
            return redirect("core:product", slug=slug)
    else:
        # add a message saying the user dosent have an order
        messages.info(request, "u don't have an active order.")
        return redirect("core:product", slug=slug)
    return redirect("core:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item qty was updated.")
            return redirect("core:order-summary")
        else:
            # add a message saying the user dosent have an order
            messages.info(request, "Item was not in your cart.")
            return redirect("core:product", slug=slug)
    else:
        # add a message saying the user dosent have an order
        messages.info(request, "u don't have an active order.")
        return redirect("core:product", slug=slug)
    return redirect("core:product", slug=slug)


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect("core:checkout")


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "Successfully added coupon")
                return redirect("core:checkout")

            except ObjectDoesNotExist:
                messages.info(request, "You do not have an active order")
                return redirect("core:checkout")


class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form': form
        }
        return render(self.request, "request_refund.html", context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            # edit the order
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()

                # store the refund
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                messages.info(self.request, "Your request was received")
                return redirect("core:request-refund")

            except ObjectDoesNotExist:
                messages.info(self.request, "This order does not exist")
                return redirect("core:request-refund")
