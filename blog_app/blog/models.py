from django.conf import settings
from django.db import models
from django.db.models.functions import Now
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    """
    Post objects manager that uses only published posts.
    """

    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    """
    Hold details and contents of the blog post.
    """

    class Keys:
        id = "id"
        title = "title"
        slug = "slug"
        author = "author"
        body = "body"
        status = "status"
        publish = "publish"
        publish_db_default = "publish_db_default"
        created = "created"
        updated = "updated"

        # object managers
        objects = "objects"
        published = "published"
        tags = "tags"

        # reverse relations
        comments = "comments"

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    class Meta:
        ordering = ["-publish"]
        indexes = [
            models.Index(fields=["-publish"]),
        ]

    title = models.CharField(max_length=254)
    slug = models.SlugField(max_length=254, unique_for_date="publish")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blog_posts",
    )
    body = models.TextField()
    status = models.CharField(max_length=32, choices=Status, default=Status.DRAFT)

    publish = models.DateTimeField(default=timezone.now)
    publish_db_default = models.DateTimeField(db_default=Now())  # Django5 db_default

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # object managers
    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()

    def get_absolute_url(self) -> str:
        return reverse(
            viewname="blog:post_detail",
            args=[self.publish.year, self.publish.month, self.publish.day, self.slug],
        )

    def __str__(self) -> str:
        return str(self.title or "")


class Comment(models.Model):
    class Keys:
        id = "id"
        name = "name"
        email = "email"
        body = "body"
        created = "created"
        updated = "updated"
        active = "active"
        post = "post"

    class Meta:
        ordering = ["created"]
        indexes = [models.Index(fields=["created"])]

    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")

    def __str__(self) -> str:
        return f"Comment by {self.name} on {self.post}"
