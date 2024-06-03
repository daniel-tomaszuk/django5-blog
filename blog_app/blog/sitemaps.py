import datetime

from django.contrib.sitemaps import Sitemap
from django.db.models import QuerySet
from django.urls import reverse
from taggit.models import Tag

from blog.models import Post


class PostSitemap(Sitemap):
    """
    Check Django docs -> ref/contrib/sitemaps/
    """

    changefreq = "weekly"
    priority = 0.9

    def items(self) -> QuerySet[Post]:
        return Post.published.all()

    def lastmod(self, obj: Post) -> datetime.datetime:
        return obj.updated

    def location(self, item: Post) -> str:
        """
        Returns item URL. Calls `get_absolute_url` by default.
        """
        location: str = super().location(item)
        return location


class TagSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self) -> QuerySet[Tag]:
        return Tag.objects.all()

    def location(self, obj) -> str:
        return reverse("blog:post_list_by_tag", args=[obj.slug])
