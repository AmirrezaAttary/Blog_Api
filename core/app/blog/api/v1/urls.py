from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

app_name = "api-v1"
router = DefaultRouter()
router.register("post", views.PostModelViewSet, basename="post")
router.register("category", views.CategoryModelViewSet, basename="category")


urlpatterns = [
    path('post-cache/<int:post_id>/', views.PostCacheAPIView.as_view(), name='post-cache'),
    path('weather/', views.WeatherAPIView.as_view(), name='weather-default'),
    path('weather/<str:city>/', views.WeatherAPIView.as_view(), name='weather-city'),
]

urlpatterns += router.urls
