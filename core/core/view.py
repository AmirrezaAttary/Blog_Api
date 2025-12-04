from django.views import View
from django.shortcuts import redirect
from django.urls import reverse

class RedirectToPostListAPI(View):
    def get(self, request, *args, **kwargs):
        return redirect(reverse("blog:post-list-api"))

    def post(self, request, *args, **kwargs):
        return redirect(reverse("blog:post-list-api"))

    def dispatch(self, request, *args, **kwargs):
        # اگه می‌خوای همه متدها (GET, POST, PUT, DELETE...) ریدایرکت بشن
        return redirect(reverse("blog:post-list-api"))
