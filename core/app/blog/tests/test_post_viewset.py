import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from app.blog.models import Post, Category
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_post_list_with_pagination(api_client):
    url = reverse("blog:api-v1:post-list")

    # ایجاد دیتا
    user = User.objects.create_user(email="u@test.com", password="pass")
    for i in range(15):
        Post.objects.create(
            author=user,
            title=f"Post {i}",
            content="content",
            status=True,
        )

    response = api_client.get(url)

    assert response.status_code == 200
    assert "results" in response.data
    assert len(response.data["results"]) == 10  # page_size=10
    assert response.data["total_objects"] == 15
    assert response.data["total_pages"] == 2


@pytest.mark.django_db
def test_post_create_requires_auth(api_client):
    url = reverse("blog:api-v1:post-list")

    payload = {
        "title": "New Post",
        "content": "Content here",
        "status": True,
        "tags": ["python"],
        "category": [],
    }

    response = api_client.post(url, payload)

    assert response.status_code == 401  # Must be authenticated


@pytest.mark.django_db
def test_post_create_authenticated(api_client):
    url = reverse("blog:api-v1:post-list")

    user = User.objects.create_user(email="test@test.com", password="pass")
    api_client.force_authenticate(user)

    category = Category.objects.create(name="Tech")

    payload = {
        "title": "My Auth Post",
        "content": "Auth content",
        "status": True,
        "tags": ["django"],
        "category": [category.id],
    }

    response = api_client.post(url, payload)

    assert response.status_code == 201
    assert response.data["title"] == "My Auth Post"
    assert response.data["author"] == user.id
    assert "snippet" in response.data


@pytest.mark.django_db
def test_post_update_only_owner(api_client):
    user1 = User.objects.create_user(email="u1@test.com", password="pass")
    user2 = User.objects.create_user(email="u2@test.com", password="pass")

    post = Post.objects.create(
        author=user1, title="My Post", content="Hello", status=True
    )

    url = reverse("blog:api-v1:post-detail", kwargs={"pk": post.pk})

    api_client.force_authenticate(user2)
    response = api_client.patch(url, {"title": "Hacked!"})

    assert response.status_code == 403  # user2 cannot edit user1’s post


@pytest.mark.django_db
def test_post_filter_by_category(api_client):
    user = User.objects.create_user(email="u@test.com", password="pass")
    api_client.force_authenticate(user)

    cat1 = Category.objects.create(name="Tech")
    cat2 = Category.objects.create(name="Life")

    p1 = Post.objects.create(author=user, title="A", content="x", status=True)
    p1.category.add(cat1)

    p2 = Post.objects.create(author=user, title="B", content="y", status=True)
    p2.category.add(cat2)

    url = reverse("blog:api-v1:post-list")

    response = api_client.get(url, {"category": cat1.id})

    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["title"] == "A"


@pytest.mark.django_db
def test_post_search(api_client):
    user = User.objects.create_user(email="u@test.com", password="pass")
    api_client.force_authenticate(user)

    Post.objects.create(author=user, title="Django Tips", content="x", status=True)
    Post.objects.create(author=user, title="Python Tricks", content="y", status=True)

    url = reverse("blog:api-v1:post-list")

    response = api_client.get(url, {"search": "Django"})

    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["title"] == "Django Tips"


@pytest.mark.django_db
def test_post_ordering(api_client):
    user = User.objects.create_user(email="u@test.com", password="pass")
    api_client.force_authenticate(user)

    Post.objects.create(author=user, title="Old", content="x", status=True)
    Post.objects.create(author=user, title="New", content="y", status=True)

    url = reverse("blog:api-v1:post-list")

    response = api_client.get(url, {"ordering": "published_date"})
    assert response.status_code == 200
