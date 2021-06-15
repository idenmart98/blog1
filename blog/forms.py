from django import forms
from .models import Post


inputAttrs = {
    'class': "form-control"
}


class LoginForm(forms.Form):
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


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs=inputAttrs))
    password = forms.CharField(widget=forms.PasswordInput(attrs=inputAttrs))
    firstName = forms.CharField(widget=forms.TextInput(attrs=inputAttrs))
    lastName = forms.CharField(widget=forms.TextInput(attrs=inputAttrs))
    email = forms.CharField(widget=forms.EmailInput(attrs=inputAttrs))


class CommentForms(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs=inputAttrs))


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'clipped_text', 'text']
        widgets = {
            'clipped_text': forms.Textarea(attrs={'rows': 3}),
        }


class RatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['rating_sum']
