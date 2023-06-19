from django import forms

from .models import Comment, Post

INPUT_STYLE = 'background: #27272a; color:white; display: block;'

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text', 'rating', )
        widgets = {
            'author': forms.fields.TextInput(attrs={
                'style': INPUT_STYLE
            }),
            'text': forms.fields.Textarea(attrs={
                'style': INPUT_STYLE + ' width: 60%; height: 80px;'
            }),
            'rating': forms.fields.Select(attrs={
                'style': INPUT_STYLE + ' padding: 10px;'
            })
        }
        labels = {
            'author': 'Your Name',
            'rating': 'How do you rate this post?',
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', )
        widgets = {
            'title': forms.fields.TextInput(attrs={
                'style': INPUT_STYLE
            }),
            'text': forms.fields.Textarea(attrs={
                'style': INPUT_STYLE + ' width: 100%;'
            })
        }