from rest_framework import viewsets
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
