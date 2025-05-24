from django import forms
from .models import Comment, User


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', )


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
