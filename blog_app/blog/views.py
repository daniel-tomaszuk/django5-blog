from django.contrib.postgres.search import SearchQuery
from django.contrib.postgres.search import SearchRank
from django.contrib.postgres.search import SearchVector
from django.core.mail import send_mail
from django.db.models import Count
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.generic import DetailView
from django.views.generic import ListView

from blog.forms import CommentForm
from blog.forms import EmailPostForm
from blog.forms import SearchForm
from blog.models import Comment
from blog.models import Post


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    template_name = "blog/post/list.html"
    paginate_by = 3

    def get_queryset(self) -> QuerySet[Post]:
        queryset: QuerySet[Post] = super().get_queryset()
        tag_slug: str = self.kwargs.get("tag_slug")
        if tag_slug:
            queryset = queryset.filter(tags__slug__in=[tag_slug])
        return queryset

    def get_context_data(self, *args, object_list=None, **kwargs) -> dict:
        context: dict = super().get_context_data(
            *args, object_list=object_list, **kwargs
        )
        context.setdefault("tag", self.kwargs.get("tag_slug"))
        return context


class PostDetailsView(DetailView):
    model = Post
    template_name = "blog/post/detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None) -> Post:
        return get_object_or_404(
            Post,
            slug=self.kwargs.get("post"),
            publish__year=self.kwargs.get("year"),
            publish__month=self.kwargs.get("month"),
            publish__day=self.kwargs.get("day"),
            status=Post.Status.PUBLISHED,
        )

    def get_context_data(self, **kwargs) -> dict:
        context: dict = super().get_context_data(**kwargs)
        comments: QuerySet[Comment] = self.object.comments.filter(active=True)
        context["comments"] = comments
        context["form"] = CommentForm()

        # get similar posts by tag
        post_tags_ids: QuerySet = self.object.tags.values_list("id", flat=True)
        similar_posts: QuerySet[Post] = Post.published.filter(
            tags__in=post_tags_ids
        ).exclude(id=self.object.id)
        similar_posts: QuerySet[Post] = similar_posts.annotate(
            same_tags_count=Count(Post.Keys.tags)
        ).order_by("-same_tags_count", "-publish")[:4]

        context["similar_posts"] = similar_posts
        return context


def post_share(request, post_id: int):
    post: Post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent: bool = False
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            validated_data: dict = form.cleaned_data
            post_url: str = request.build_absolute_uri(post.get_absolute_url())
            subject: str = (
                f"{validated_data['name']} at {validated_data['email']} recommends you read {post.title}"
            )
            message: str = (
                f"Read {post.title} at {post_url}\n\n"
                f"{validated_data['name']}'s comments: {validated_data['comments']}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[validated_data["to"]],
            )
            sent = True
    else:
        form = EmailPostForm()

    return render(
        request=request,
        template_name="blog/post/share.html",
        context=dict(post=post, form=form, sent=sent),
    )


@require_POST
def post_comment(request, post_id: int):
    post: Post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED,
    )
    comment = None
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(
        request=request,
        template_name="blog/post/comment.html",
        context=dict(post=post, form=form, comment=comment),
    )


def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query: str = form.cleaned_data.get("query")
            search_vector = SearchVector(Post.Keys.title, weight="A") + SearchVector(
                Post.Keys.body, weight="B"
            )

            search_query = SearchQuery(query)

            # it's possible to pass additional config
            # check postgres github - master/scr/backend/snowball/stopwords/
            # search_vector = SearchVector(Post.Keys.title, Post.Keys.body, config="spanish")
            # search_query = SearchQuery(query, config="spanish")

            results: QuerySet[Post] = (
                Post.published.annotate(
                    search=search_vector,
                    rank=SearchRank(search_vector, search_query),
                )
                .filter(search=search_query, rank__gte=0.3)
                .order_by("-rank")
            )

    return render(
        request=request,
        template_name="blog/post/search.html",
        context=dict(
            form=form,
            query=query,
            results=results,
        ),
    )
