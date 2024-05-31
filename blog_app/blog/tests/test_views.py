from typing import Callable

import pytest
from django.urls import reverse

from blog.factories import PostFactory
from blog.models import Post


@pytest.mark.django_db
class TestPostViews:
    SETUP_POSTS_COUNT = 2

    def setup_method(self, method: Callable):
        for _ in range(self.SETUP_POSTS_COUNT):
            PostFactory()

        for _ in range(self.SETUP_POSTS_COUNT + 1):
            PostFactory(status=Post.Status.PUBLISHED)

    def test_list_posts__published_posts_only(self, client):
        url: str = reverse("create-short-url")
        response = client.get(url)
        pass

    def test_get_post_details(self, client):
        pass

    def test_get_post_details__published_only(self, client):
        pass

    def test_get_post_details__not_found(self, client):
        pass
