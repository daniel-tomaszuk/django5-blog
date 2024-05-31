from typing import Callable

import pytest

from blog.factories import PostFactory
from blog.models import Post


@pytest.mark.django_db
class TestPostModel:
    SETUP_POSTS_COUNT = 2

    def setup_method(self, method: Callable):
        for _ in range(self.SETUP_POSTS_COUNT):
            PostFactory()

        for _ in range(self.SETUP_POSTS_COUNT + 1):
            PostFactory(status=Post.Status.PUBLISHED)

    def test_post_managers__objects_count_as_expected(self):
        all_posts_count: int = Post.objects.count()
        published_posts_count: int = Post.published.count()

        assert all_posts_count == 2 * self.SETUP_POSTS_COUNT + 1
        assert published_posts_count == self.SETUP_POSTS_COUNT + 1
