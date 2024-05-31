from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.views.generic import ListView

from blog.models import Post


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    template_name = "blog/post/list.html"
    paginate_by = 3


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
