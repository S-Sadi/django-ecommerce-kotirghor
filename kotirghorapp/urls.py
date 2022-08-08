from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("product", views.product, name="product"),
    path("payment", views.payment, name="payment"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("register", views.register, name="register"),
    path("about", views.about, name="about"),
    path("contact", views.contact, name="contact"),
    path("PrivacyAndPolicy", views.privacy, name="privacy"),
    path("TermsAndConditions", views.terms, name="terms"),
    path("search", views.search_htm, name="search"),
    path("cart/<int:slug>", views.cart, name="cart"),
    path("addtocart/<int:slug>", views.addtocart, name="addtocart")
]