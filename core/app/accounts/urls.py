from django.urls import path,include
from django.contrib.auth.views import LogoutView
from .views import CustomLoginView, RegisterPage, send_email


app_name = "accounts"

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
    path("register/", RegisterPage.as_view(), name="register"),
    path('sendEmail',send_email,name='send_email'),
    path('api/v1/',include('app.accounts.api.v1.urls'))
]