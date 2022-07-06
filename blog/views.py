from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from PIL import Image

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# posts = [
#     {
#         'author': 'Apurva',
#         'title': 'Blog Post 1',
#         'content': 'First post content',
#         'date_posted': 'July 23, 2021',
#     },
#     {
#         'author': 'Varad',
#         'title': 'Blog Post 2',
#         'content': 'Second post content',
#         'date_posted': 'August 1, 2021',
#     }
# ]

# <app>/<model>_<type>.html


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']  # latest post seen above


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def home(request):
    context = {
        # 'posts': posts
        'posts': Post.objects.all()
    }
    # return HttpResponse('<h1>BlogIt Home</h1>')
    return render(request, 'blog/home.html', context)


def about(request):
    # return HttpResponse('<h1>BlogIt About</h1>')
    return render(request, 'blog/about.html', {'title': 'About'})
