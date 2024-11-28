from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST

from posts.forms import CreatePostForm, CommentCreateForm
from posts.models import Post, PostView, Comment


class AdminPostApprovalView(View):

    def get(self, request):
        posts = Post.objects.filter(status=Post.Status.DRAFT)
        context = {
            "posts": posts
        }
        return render(request, "admin_approval.html", context)

    def post(self, request):
        post_id = request.POST.get("post_id")
        post = get_object_or_404(Post, id=post_id)
        post.status = Post.Status.PUBLISHED
        post.save()
        return redirect("admin_approval")


class PostCommentView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        comment_form = CommentCreateForm(data=request.POST)
        if comment_form.is_valid():
            Comment.objects.create(
                user=request.user,
                post=post,
                text=comment_form.cleaned_data['text']
            )
            return redirect(reverse('posts:detail', kwargs={"pk": post.id}))
        context = {
            'post': post,
            'comment_form': comment_form
        }
        return render(request, 'detail.html', context)


class PostListView(View):
    def get(self, request):
        category_name = request.GET.get('name', None)
        posts = Post.objects.filter(
            status=Post.Status.PUBLISHED,
            category__name=category_name
        ) if category_name else Post.objects.filter(status=Post.Status.PUBLISHED)
        context = {
            'posts': posts
        }
        return render(request, 'list.html', context)



class CreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = CreatePostForm()
        context = {
            'form': form
        }
        return render(request, 'create.html', context)

    def post(self, request):
        form = CreatePostForm(
            data=request.POST,
            files=request.FILES
        )
        if form.is_valid():
            post_instance = form.save(commit=False)
            post_instance.user = request.user
            post_instance.save()
            return redirect('common:home')
        context = {
            "form": form
        }
        return render(request, 'create.html', context)


class DetailView(View):
    def get(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        comment_form = CommentCreateForm()
        user = request.user
        if user.is_authenticated:
            post_view, created = PostView.objects.get_or_create(post=post, user=user)
            if created:
                post.view_count += 1
                post.save()
        context = {
            "post": post,
            'comment_form': comment_form
        }
        return render(request, 'detail.html', context)


class UpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        # Faqat post egasiga ruxsat berish
        if post.user != request.user:
            return redirect('common:home')
        form = CreatePostForm(instance=post)
        context = {
            "form": form
        }
        return render(request, 'update.html', context)

    def post(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        if post.user != request.user:
            return redirect('common:home')
        form = CreatePostForm(
            data=request.POST,
            files=request.FILES,
            instance=post
        )
        if form.is_valid():
            form.save()
            return redirect(reverse('posts:detail', kwargs={"pk": post.id}))
        context = {
            "form": form
        }
        return render(request, 'update.html', context)


class DeleteView(View, LoginRequiredMixin):

    def post(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        if post.user == request.user:
            post.delete()
        return redirect('common:home')
