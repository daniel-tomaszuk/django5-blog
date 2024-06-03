import datetime

from django.contrib.sitemaps import Sitemap
from django.db.models import QuerySet

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
