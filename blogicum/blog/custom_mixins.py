from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class CustomAuthorMixin(UserPassesTestMixin):
    """Миксин для проверки, что текущий пользователь
    является автором.
    """

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def handle_no_permission(self):
        obj = self.get_object()
        return redirect('blog:post_detail', post_id=obj.pk)
