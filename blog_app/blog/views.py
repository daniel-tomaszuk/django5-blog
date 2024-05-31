from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from blog.models import Post


def list_posts(request):
    published_posts: QuerySet[Post] = Post.published.all()
    return render(
        request=request,
        template_name="blog/post/list.html",
        context=dict(posts=published_posts),
    )


def get_post_details(request, post_id: int):
    post: Post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    return render(
        request=request, template_name="blog/post/detail.html", context=dict(post=post)
    )
