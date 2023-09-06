from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage.as_view(), name="home-page"),
    path('register/', views.regesterFormView.as_view(), name="register-form"),
    path('create-address/', views.addressFormView.as_view(), name="create-address"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),
    path('checkout/', views.checkout, name="checkout"),
    path('payment/', views.payment, name="payment"),
    path('add-to-cart/', views.addToCart),
    path('secret/', views.secret, name="secret")

]