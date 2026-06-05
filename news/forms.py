from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text']  # Без post_type
        widgets = {
            'text': forms.Textarea(attrs={'rows': 10, 'cols': 80}),
        }