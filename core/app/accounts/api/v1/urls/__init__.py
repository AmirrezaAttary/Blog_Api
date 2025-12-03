from django.urls import path, include

urlpatterns = [
    path('',include('app.accounts.api.v1.urls.accounts')),
    path('profile',include('app.accounts.api.v1.urls.profiles'))
]