from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy


class CustomAuthorMixin(UserPassesTestMixin):
    
    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user
    
    def handle_no_permission(self):
        object = self.get_object()
        return redirect('blog:post_detail', post_id=object.pk)
    
    # def get_success_url(self):
    #     return reverse_lazy(
    #         'blog:post_detail', kwargs={'post_id': self.object.pk}
    #     )
