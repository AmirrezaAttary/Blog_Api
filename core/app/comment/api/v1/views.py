from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ...models import Comment
from .serializers import CommentSerializers
from .paginations import LargeResultsSetPagination


class CommentModelViewSet(viewsets.ModelViewSet):
    """getting a list of comments and creating new comments"""

    serializer_class = CommentSerializers
    pagination_class = LargeResultsSetPagination
    queryset = Comment.objects.filter(approved=True)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["post", "email", "approved"]
    search_fields = ["post__title", "subject"]
    ordering_fields = ["created_date"]
