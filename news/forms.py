from django import forms
from .models import Post, Category

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text']  # Без post_type
        widgets = {
            'text': forms.Textarea(attrs={'rows': 10, 'cols': 80}),
        }


class SubscriptionForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label='Выберите категорию',
        widget=forms.Select(attrs={'class': 'form-control'})
    )