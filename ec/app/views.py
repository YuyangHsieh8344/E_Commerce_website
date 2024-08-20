from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.contrib import messages
from .models import  OrderPlaced, Payment, Product, Customer, Cart
from .forms import CustomerRegistrationForm, CustomerProfileForm

#added area
from django.contrib.auth import logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.views.decorators.http import require_POST
from django.db.models import Q


from django.conf import settings
import paypalrestsdk

from django.http import JsonResponse
import json

from django.views.generic import TemplateView

# Home view - renders the home page
def home(request):
    return render(request, "app/home.html")

# About view - renders the about page
def about(request):
    return render(request, "app/about.html")

# Contact view - renders the contact page
def contact(request):
    return render(request, "app/contact.html")

# CategoryView - Displays products based on their category
class CategoryView(View):
    def get(self, request, val):
        # Filter products by category
        products = Product.objects.filter(category=val)
        # Get titles of products in the same category
        titles = Product.objects.filter(category=val).values('title')
        return render(request, "app/category.html", {'product': products, 'title': titles})

# CategoryTitle - Displays products based on their title
class CategoryTitle(View):
    def get(self, request, val):
        print(f"Received category value: {val}")  # Debug print
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request, "app/category.html", locals())



# ProductDetail - Displays the details of a specific product
class ProductDetail(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        category = product.category  # Fetch category related to the product
        referer_url = request.META.get('HTTP_REFERER', '/')  # Get the referring URL, default to '/' if not found
        return render(request, "app/productdetail.html", {'product': product, 'category': category, 'referer_url': referer_url})

    

# CustomerRegistrationView - Handles customer registration
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()  # Initialize an empty registration form
        return render(request, "app/customerregistration.html", {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)  # Populate form with POST data
        if form.is_valid():
            form.save()  # Save the new customer
            messages.success(request, "Account Created!!")  # Display success message
            return redirect('account_created')  # Redirect to the success page
        else:
            messages.warning(request, "Invalid Input Data")  # Display error message if form is invalid
        return render(request, "app/customerregistration.html", {'form': form})
        

# ProfileView - Handles displaying and updating the user's profile
class ProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            # Flash a message to be displayed on the login page
            messages.info(request, "Please log in to view your profile.")
            return redirect('login')

        try:
            customer = Customer.objects.get(user=request.user)
            form = CustomerProfileForm(instance=customer)
        except Customer.DoesNotExist:
            customer = None
            form = CustomerProfileForm()

        return render(request, "app/profile.html", {'form': form, 'customer': customer})

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        try:
            customer = Customer.objects.get(user=request.user)
            form = CustomerProfileForm(request.POST, instance=customer)
        except Customer.DoesNotExist:
            form = CustomerProfileForm(request.POST)

        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = request.user
            customer.save()
            messages.success(request, "Profile saved successfully!")
            return redirect('profile')
        else:
            messages.error(request, "Failed to save profile. Please correct the errors below.")
        return render(request, "app/profile.html", {'form': form, 'customer': customer})


class EditProfileView(View):
    def get(self, request):
        # Get the current user's customer profile data
        try:
            customer = Customer.objects.get(user=request.user)
            form = CustomerProfileForm(instance=customer)
        except Customer.DoesNotExist:
            form = CustomerProfileForm()
        
        return render(request, "app/edit_profile.html", {'form': form})

    def post(self, request):
        try:
            customer = Customer.objects.get(user=request.user)
            form = CustomerProfileForm(request.POST, instance=customer)
        except Customer.DoesNotExist:
            # Create a new form instance with POST data
            form = CustomerProfileForm(request.POST)
            customer = None
        
        if form.is_valid():
            customer_profile = form.save(commit=False)
            if not customer:
                # If no existing customer, set the user field
                customer_profile.user = request.user
            customer_profile.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')  # Redirect to the profile page after saving
        else:
            messages.error(request, "Failed to update profile. Please correct the errors below.")
        
        return render(request, "app/edit_profile.html", {'form': form})

# UserLogout - Handles user logout and redirects to login page
class UserLogout(View):
    def get(self, request):
        logout(request)  # Log out the user
        messages.success(request, "You have been logged out successfully.")  # Display success message
        return redirect('login')  # Redirect to the login page after logout
    

class AccountCreatedView(View):
    def get(self, request):
        return render(request, "app/account_created.html")
    

@require_POST
@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.POST.get('prod_id')
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    category_id = request.POST.get('category_id')
    if category_id:
        request.session['last_category'] = category_id

    return redirect("show_cart")

@login_required
def show_cart(request):
    cart = Cart.objects.filter(user=request.user)
    amount = sum(item.quantity * item.product.discounted_price for item in cart)
    totalamount = amount  # You might want to add shipping or tax here

    #referer_url = request.META.get('HTTP_REFERER', '/')
    last_category = request.session.get('last_category')
    back_url = reverse('category', args=[last_category]) if last_category else '/'

    context = {
        'cart': cart,
        'amount': amount,
        'totalamount': totalamount,
        'back_url': back_url,
        #'referer_url': referer_url,
    }
    return render(request, 'app/addtocart.html', context)

def plus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount 
        #print(prod_id)
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    

def minus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount 
        #print(prod_id)
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    

def remove_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount 
        #print(prod_id)
        data={
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    

class CheckoutView(View):
    def get(self, request):
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        
        # Calculate total amount
        total_amount = sum(item.quantity * item.product.discounted_price for item in cart_items)
        
        # Get the user's addresses
        addresses = Customer.objects.filter(user=user)
        
        # Pass the PayPal client ID from settings to the template
        paypal_client_id = settings.PAYPAL_CLIENT_ID
        
        # Render the checkout page with the necessary context
        return render(request, 'app/checkout.html', {
            'cart_items': cart_items,
            'totalamount': total_amount,
            'addresses': addresses,
            'PAYPAL_CLIENT_ID': paypal_client_id,
        })

        
class PaymentSuccessView(TemplateView):
    template_name = 'app/payment_success.html'

class PaymentFailedView(TemplateView):
    template_name = 'app/payment_failed.html'


@login_required
def payment_complete(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            total_amount = data.get('totalAmount')
            payment_id = data.get('paymentId')  # Assuming you receive this from the payment gateway

            # Create a Payment instance
            payment = Payment.objects.create(
                user=request.user,
                amount=total_amount,
                paypal_payment_id=payment_id,
                paid=True
            )

            # Get all cart items for the user
            cart_items = Cart.objects.filter(user=request.user)

            # Create OrderPlaced instances for each cart item
            for item in cart_items:
                OrderPlaced.objects.create(
                    user=request.user,
                    customer=item.product.customer,  # Assuming you have a way to get customer for the product
                    product=item.product,
                    quantity=item.quantity,
                    payment=payment
                )

            # Clear the user's cart
            cart_items.delete()

            # Redirect to payment success page
            return render(request, 'payment_success.html', {'payment': payment})

        except Exception as e:
            # If any error occurs during the process, redirect to payment failed page
            return render(request, 'payment_failed.html', {'error': str(e)})

    # If the request method is not POST, redirect to payment failed page
    return render(request, 'payment_failed.html', {'error': 'Invalid request method'})
