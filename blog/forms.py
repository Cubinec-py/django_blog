from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin


from blog.models import PostCustomUser, Comment


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = PostCustomUser
        fields = ['username', 'password']


class CustomUserCreationForm(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = PostCustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def clean_password(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password1


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'comment_body']


class ContactCreateForm(forms.Form):
    email = forms.EmailField(required=True)
    subject = forms.CharField(max_length=255)
    text = forms.CharField(widget=forms.Textarea, help_text='Write your problem')
