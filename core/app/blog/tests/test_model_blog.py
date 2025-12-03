import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from app.blog.models import Post, Category

User = get_user_model()


@pytest.mark.django_db
def test_category_str():
    category = Category.objects.create(name="Tech")
    assert str(category) == "Tech"


@pytest.mark.django_db
def test_post_str():
    user = User.objects.create_user(email="test@test.com", password="pass1234")
    post = Post.objects.create(
        author=user,
        title="My Post",
        content="Hello world content",
        status=True,
    )
    assert str(post) == "My Post"


@pytest.mark.django_db
def test_post_creation_with_category():
    user = User.objects.create_user(email="user@test.com", password="pass1234")
    category1 = Category.objects.create(name="Science")
    category2 = Category.objects.create(name="Tech")

    post = Post.objects.create(
        author=user,
        title="Post with Categories",
        content="Some content",
    )
    post.category.add(category1, category2)

    assert post.category.count() == 2
    assert category1 in post.category.all()
    assert category2 in post.category.all()


@pytest.mark.django_db
def test_post_tags():
    user = User.objects.create_user(email="tag@test.com", password="pass1234")
    post = Post.objects.create(
        author=user,
        title="Tagged Post",
        content="Tag test content",
    )
    post.tags.add("python", "django")

    assert post.tags.count() == 2
    assert "python" in post.tags.names()
    assert "django" in post.tags.names()


@pytest.mark.django_db
def test_post_get_snippet():
    user = User.objects.create_user(email="snippet@test.com", password="pass1234")
    post = Post.objects.create(
        author=user,
        title="Snippet Post",
        content="HelloWorld",
    )

    assert post.get_snippet() == "Hello..."


@pytest.mark.django_db
def test_post_get_absolute_api_url(client):
    user = User.objects.create_user(email="api@test.com", password="pass1234")
    post = Post.objects.create(
        author=user,
        title="API URL Post",
        content="Content here",
    )

    url = post.get_absolute_api_url()
    expected = reverse("blog:api-v1:post-detail", kwargs={"pk": post.pk})

    assert url == expected
