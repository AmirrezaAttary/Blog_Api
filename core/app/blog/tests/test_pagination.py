import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from app.blog.models import Post, Category

User = get_user_model()


@pytest.mark.django_db
def test_large_results_pagination_structure(api_client):
    user = User.objects.create_user(email="u@test.com", password="pass")

    for i in range(12):
        Post.objects.create(author=user, title=f"P{i}", content="x", status=True)

    url = reverse("blog:api-v1:post-list")
    response = api_client.get(url)

    assert response.status_code == 200
    assert "links" in response.data
    assert "next" in response.data["links"]
    assert "previous" in response.data["links"]
    assert "total_objects" in response.data
    assert "total_pages" in response.data
    assert "results" in response.data
