import pytest
from django.urls import reverse
from app.blog.models import Category
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_category_list(api_client):
    Category.objects.create(name="Tech")
    Category.objects.create(name="Science")

    url = reverse("blog:api-v1:category-list")

    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data["results"]) == 2


@pytest.mark.django_db
def test_category_create_requires_auth(api_client):
    url = reverse("blog:api-v1:category-list")
    response = api_client.post(url, {"name": "NewCat"})
    assert response.status_code == 401


@pytest.mark.django_db
def test_category_create_authenticated(api_client):
    user = User.objects.create_user(email="c@test.com", password="pass")
    api_client.force_authenticate(user)

    url = reverse("blog:api-v1:category-list")

    response = api_client.post(url, {"name": "Tech"})

    assert response.status_code == 201
    assert response.data["name"] == "Tech"
