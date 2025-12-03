from django.urls import path, include
from . import views

app_name = "comment"

urlpatterns = [
    path("api/v1/", include("app.comment.api.v1.urls")),
]
