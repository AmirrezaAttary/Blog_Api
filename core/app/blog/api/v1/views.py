import requests
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.conf import settings
from rest_framework import viewsets,status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ...models import Post, Category
from .serializers import PostSerializer, CategorySerializer
from .paginations import LargeResultsSetPagination
from .permissions import IsOwnerOrReadOnly


# Example for ViewSet in Django CBV
class PostModelViewSet(viewsets.ModelViewSet):
    """getting a list of posts and creating new posts"""

    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = PostSerializer
    pagination_class = LargeResultsSetPagination
    queryset = Post.objects.filter(status=True)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["category", "author", "status"]
    search_fields = ["title", "content"]
    ordering_fields = ["published_date"]


class CategoryModelViewSet(viewsets.ModelViewSet):
    """getting a list of categories and creating new categories"""
    
    pagination_class = LargeResultsSetPagination 
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()



@method_decorator(cache_page(60 * 20), name='dispatch')  # کش 20 دقیقه
class PostCacheAPIView(APIView):
    """
    دریافت اطلاعات پست از آدرس مشخص و کش آن به مدت 20 دقیقه
    """

    def get(self, request, post_id):
        url = f'https://manmarket.ir/blog/api/v1/post/{post_id}/'

        try:
            response = requests.get(url)
        except requests.exceptions.RequestException:
            return Response({'error': 'عدم دسترسی به سرویس خارجی'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        if response.status_code == 200:
            data = response.json()
            # می‌توانیم فقط فیلدهای مورد نیاز را برگردانیم
            result = {
                'id': data.get('id'),
                'title': data.get('title'),
                'snippet': data.get('snippet'),
                'content': data.get('content'),
                'author': data.get('author'),
                'category': data.get('category'),
                'tags': data.get('tags'),
                'status': data.get('status'),
                'published_date': data.get('published_date'),
            }
            return Response(result)

        return Response({'error': 'پست یافت نشد'}, status=status.HTTP_404_NOT_FOUND)
    
@method_decorator(cache_page(60 * 20), name='dispatch')  # کش 20 دقیقه
class WeatherAPIView(APIView):
    """
    دریافت وضعیت آب‌وهوا برای یک شهر
    """

    def get(self, request, city="تهران"):
        api_key = settings.OPENWEATHER_API_KEY
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=fa'

        try:
            response = requests.get(url)
        except requests.exceptions.RequestException:
            return Response({'error': 'عدم دسترسی به سرویس خارجی'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        if response.status_code == 200:
            data = response.json()
            result = {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed']
            }
            return Response(result)

        return Response({'error': 'شهر یافت نشد'}, status=status.HTTP_404_NOT_FOUND)
