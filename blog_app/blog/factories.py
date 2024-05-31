import factory
from common.factories import UserFactory

from blog.models import Post


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.Faker("word")
    slug = factory.Faker("word")
    author = factory.SubFactory(UserFactory)
    body = factory.Faker("text")
    status = Post.Status.DRAFT
