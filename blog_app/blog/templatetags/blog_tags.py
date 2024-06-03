from django import template
from django.db.models import Count
from django.db.models import QuerySet

from blog.models import Post

register = template.Library()


@register.simple_tag
def total_posts() -> int:
    """
    Simple template tag that returns total count of published posts.
    """
    return Post.published.count()


@register.inclusion_tag("blog/post/latest_posts.html")
def show_latest_posts(count: int = 5) -> dict:
    """
    Inclusion template tag.
    Renders HTML template using context defined in the tag.
    """
    latest_posts: QuerySet[Post] = Post.published.order_by("-publish").only(
        Post.Keys.title
    )[:count]
    return dict(latest_posts=latest_posts)


@register.simple_tag
def get_most_commented_posts(count: int = 5) -> QuerySet[Post]:
    """
    Template tag that returns query set.
    """
    return (
        Post.published.annotate(total_comments=Count(Post.Keys.comments))
        .only(Post.Keys.title)
        .order_by("-total_comments")[:count]
    )
