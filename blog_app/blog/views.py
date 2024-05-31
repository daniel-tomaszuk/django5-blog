import contextlib

from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from blog.models import Post


def list_posts(request):
    published_posts: QuerySet[Post] = Post.published.all()
    paginator = Paginator(object_list=published_posts, per_page=2)
    page_number: str = request.GET.get("page")

    try:
        published_posts = paginator.page(page_number)
    except PageNotAnInteger:
        # return first page if it's not possible to cast into integer
        published_posts = paginator.page(1)
    except EmptyPage:
        # return last page if passed page number does not exists
        published_posts = paginator.page(paginator.num_pages)
    return render(
        request=request,
        template_name="blog/post/list.html",
        context=dict(posts=published_posts),
    )


def get_post_details(request, year: int, month: int, day: int, post: str):
    post: Post = get_object_or_404(
        Post,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        status=Post.Status.PUBLISHED,
    )
    return render(
        request=request, template_name="blog/post/detail.html", context=dict(post=post)
    )
