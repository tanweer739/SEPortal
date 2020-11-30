from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Post, Comment
from .forms import CommentForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


# Create your views here.


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'activitystream/home.html'  # <app>/<model>_<view_type>.html
    context_object_name = 'posts'
    paginate_by = 2


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'activitystream/user_posts.html'  # <app>/<model>_<view_type>.html
    context_object_name = 'posts'
    paginate_by = 2

    # returns specific query set to be used in template similar to get_context_date except it doesn't return multiple
    # dictionary keys
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object).all()
        return context


class PostUpdateView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'document']
    success_message = 'Post is successfully Updated'

    # override for current logged in user

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # throw an 403 forbidden error if post does not belong to the current user
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(UserPassesTestMixin, DeleteView):
    model = Post
    success_message = 'Post is successfully Deleted'

    def get_success_url(self):
        return reverse_lazy('user-posts', kwargs={'username': self.object.author})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    # overriding delete method just to make success message work , SuccessMessageMixin is not supported in DeleteViews.
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'document']
    success_message = 'Post is successfully made'

    # override for current logged in user
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, 'Comment is successfully made')
            return redirect('post-detail', pk=pk)
    else:
        form = CommentForm(user=request.user)
    return render(request, 'activitystream/add_comment.html', {'form': form})


class CommentUpdateView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['content', 'document']
    success_message = 'Comment is successfully Updated'

    # override for current logged in user

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    success_message = 'Comment is successfully Deleted'

    # overriding success url for to the current post
    def get_success_url(self):
        post = self.object.post
        return reverse_lazy('post-detail', kwargs={'pk': post.id})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    # overriding delete method just to make success message work , SuccessMessageMixin is not supported in DeleteViews.
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
