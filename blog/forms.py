from django import forms
from .models import Post
from django.contrib.auth import get_user_model

User = get_user_model()


inputAttrs = {
    'class': "form-control"
}


class LoginForm(forms.ModelForm):
    username = forms.CharField(
        label='Username',
        max_length=100,
        widget=forms.TextInput(attrs=inputAttrs)
    )
    password = forms.CharField(
        label='Password',
        max_length=64,
        widget=forms.PasswordInput(attrs=inputAttrs)
    )
    class Meta:
        model = User
        fields = ['username','password']


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','password','email','first_name', 'last_name']


class CommentForms(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs=inputAttrs))


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'clipped_text', 'text', 'category']
        widgets = {
            'clipped_text': forms.Textarea(attrs={'rows': 3}),
        }


class RatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['rating_sum']
