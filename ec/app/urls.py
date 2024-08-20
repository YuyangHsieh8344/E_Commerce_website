from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordResetForm, MyPasswordChangeForm, MySetPasswordForm
from .views import  PaymentFailedView, PaymentSuccessView, UserLogout

#from .views import CustomLoginView
from django.views.generic import TemplateView


urlpatterns = [
    path("", views.home, name='home'),  # Home page
    path("about", views.about, name='about'),  # About page
    path("contact", views.contact, name='contact'),  # Contact page

    path("profile/", views.ProfileView.as_view(), name='profile'),  # profile page
    path("address/", views.ProfileView.as_view(), name='address'),  # address page
    path("edit-profile/", views.EditProfileView.as_view(), name='edit-profile'),

    path("category/<slug:val>/", views.CategoryView.as_view(), name='category'),  # Category view by slug
    path("category-title/<val>/", views.CategoryTitle.as_view(), name='category-title'),  # Category title view by value
    path("product-detail/<int:pk>/", views.ProductDetail.as_view(), name='product-detail'),  # Product detail view by ID

    path('category-title/<str:val>/', views.CategoryTitle.as_view(), name='category-title'),

    # Sign Up
    path("registration/", views.CustomerRegistrationView.as_view(), name='customerregistration'),

    # login 
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'),
    
    #logout
    path('logout/', UserLogout.as_view(), name='logout'),

    # password change
    path("passwordchange/", auth_views.PasswordChangeView.as_view(template_name='app/changepassword.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name='passwordchange'),

    # password change done
    path("passwordchangedone/", auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),

    # Password reset
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name='app/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),

    # Password reset done
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),

    # Password reset confirm
    path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),

    # Password reset complete
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),

    #accounted created
    path("account-created/", views.AccountCreatedView.as_view(), name='account_created'),

    #add to cart
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),

    #show cart
    path('cart/', views.show_cart, name='show_cart'),

    #checkout
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),

    path('pluscart/', views.plus_cart),

    path('minuscart/', views.minus_cart),

    path('removecart/', views.remove_cart),

    #path('app/orderplaced/', views.OrderPlacedView.as_view(), name='order_placed'),

    path('payment-complete/', views.payment_complete, name='payment_complete'),

    path('payment-success/', PaymentSuccessView.as_view(), name='payment_success'),
    path('payment-failed/', PaymentFailedView.as_view(), name='payment_failed'),
   
    path('', include('paypal.standard.ipn.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
