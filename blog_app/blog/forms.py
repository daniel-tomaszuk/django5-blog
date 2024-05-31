from django import forms

from blog.models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(
        required=False,
        max_length=254,
        widget=forms.Textarea,
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (Comment.Keys.name, Comment.Keys.email, Comment.Keys.body)
