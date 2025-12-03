from django.shortcuts import render
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from .models import Post
from .forms import PostForm
from django.shortcuts import get_list_or_404
from django.http import HttpResponse


# Create your views here.


class IndexView(TemplateView):
    """
    a class based view to show index page
    """

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "ali"
        context["posts"] = Post.objects.all()
        return context


class RedirectToMaktab(RedirectView):
    url = "https://maktabkhooneh.org"

    def get_redirect_url(self, *args, **kwargs):
        post = get_list_or_404(Post, pk=kwargs["pk"])
        print(post)
        return super().get_redirect_url(*args, **kwargs)


class PostListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = "blog.view_post"
    model = Post
    context_object_name = "posts"
    # paginate_by = 2
    ordering = "-id"

    # def get_queryset(self):
    #     posts = Post.objects.filter(status=False)
    #     return posts
    
    
class PostListApiView(TemplateView):
    template_name = "blog/post_list_api.html"


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    success_url = "/blog/post"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostEditView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    success_url = "/blog/post"


class PostDeleteView(DeleteView):
    model = Post
    success_url = "/blog/post"
