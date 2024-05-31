from django.urls import path

from blog.views import PostDetailsView
from blog.views import PostListView

app_name = "blog"

urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>/",
        PostDetailsView.as_view(),
        name="post_detail",
    ),
]
