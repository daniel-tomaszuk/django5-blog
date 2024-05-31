from django.urls import path

from blog import views

app_name = "blog"

urlpatterns = [
    path("", views.list_posts, name="post_list"),
    path("<int:post_id>/", views.get_post_details, name="post_detail"),
]
