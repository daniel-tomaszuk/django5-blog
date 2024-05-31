from django.contrib import admin

from blog.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        Post.Keys.title,
        Post.Keys.slug,
        Post.Keys.author,
        Post.Keys.publish,
        Post.Keys.status,
    )
    list_filter = (
        Post.Keys.status,
        Post.Keys.created,
        Post.Keys.publish,
        Post.Keys.author,
    )
    search_fields = (Post.Keys.title, Post.Keys.body)
    prepopulated_fields = {Post.Keys.slug: (Post.Keys.title,)}
    raw_id_fields = (Post.Keys.author,)
    date_hierarchy = Post.Keys.publish
    ordering = (Post.Keys.status, Post.Keys.publish)

    # Django5 facet filter counts
    show_facets = admin.ShowFacets.ALLOW
