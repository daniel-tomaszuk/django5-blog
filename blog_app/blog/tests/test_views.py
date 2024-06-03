from typing import Callable

import pytest
from django.urls import reverse

from blog.factories import PostFactory
from blog.models import Post


@pytest.mark.django_db
class TestPostViews:
    SETUP_POSTS_COUNT = 2

    @classmethod
    def setup_class(cls):
        cls.list_url = reverse("blog:post_list")

    def setup_method(self, method: Callable):
        for _ in range(self.SETUP_POSTS_COUNT):
            PostFactory()

        for _ in range(self.SETUP_POSTS_COUNT + 1):
            PostFactory(status=Post.Status.PUBLISHED)

    def test_list_posts__published_posts_only(self, client):
        response = client.get(self.list_url)
        pass

    def test_get_post_details(self, client):
        pass

    def test_get_post_details__published_only(self, client):
        pass

    def test_get_post_details__not_found(self, client):
        pass

    def test_post_absolute_url(self):
        pass

    def test_pagination__empty_page(self):
        pass

    def test_pagination__page_not_an_integer(self):
        pass

    def test_get_post_by_tag_slug(self):
        pass
