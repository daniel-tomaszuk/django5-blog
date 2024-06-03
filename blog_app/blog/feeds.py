import datetime

import markdown
from django.contrib.syndication.views import Feed
from django.db.models import QuerySet
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy

from blog.models import Post


class LatestPostsFeed(Feed):
    """
    Check Django docs - ref/contrib/syndication/
    """

    DEFAULT_POSTS_COUNT = 5

    title = "My blog"
    link = reverse_lazy("blog:post_list")
    description = "My new posts"

    def items(self) -> QuerySet[Post]:
        return Post.published.all()[: self.DEFAULT_POSTS_COUNT]

    def item_title(self, item: Post) -> str:
        return item.title

    def item_description(self, item: Post) -> str:
        return truncatewords_html(markdown.markdown(item.body), 30)

    def item_pubdate(self, item: Post) -> datetime.datetime:
        return item.publish
