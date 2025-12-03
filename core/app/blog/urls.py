from django.urls import path, include
from . import views

app_name = "blog"

urlpatterns = [
    # path("cbv", views.IndexView.as_view(),name='cbv-index'),
    path("post/", views.PostListView.as_view(), name="post-list"),
    path("post/api/", views.PostListApiView.as_view(), name="post-list-api"),
    path("redi/<int:pk>", views.RedirectToMaktab.as_view(), name="redi"),
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("post/create/", views.PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/edit", views.PostEditView.as_view(), name="post-edit"),
    path(
        "post/<int:pk>/delete",
        views.PostDeleteView.as_view(),
        name="post-delete",
    ),
    path("api/v1/", include("app.blog.api.v1.urls")),
]
