from datetime import timedelta

from django.utils import timezone
from django.shortcuts import render
from django.views import View

from posts.models import Post


class HomePageView(View):
    def get(self, request):
        now = timezone.now()
        last_week = now - timedelta(days=7)
        last_month = now - timedelta(days=30)

        latest_post = Post.objects.filter(status=Post.Status.PUBLISHED).order_by('-created_time')[:5]
        most_view_post = Post.objects.filter(status=Post.Status.PUBLISHED).order_by('-view_count')[:5]
        popular_this_week = Post.objects.filter(status=Post.Status.PUBLISHED, created_time__gte=last_week).order_by(
            '-view_count')[:5]
        popular_this_month = Post.objects.filter(status=Post.Status.PUBLISHED, created_time__gt=last_month).order_by(
            '-view_count')[:5]
        posts = Post.objects.filter(status=Post.Status.PUBLISHED).order_by('-created_time')
        recommended_post = Post.objects.filter(status=Post.Status.PUBLISHED, is_recommended=True)[:5]

        context = {
            "posts": posts,
            'latest_post': latest_post,
            'most_view_post': most_view_post,
            'popular_this_week': popular_this_week,
            'popular_this_month': popular_this_month,
            'recommended_post': recommended_post
        }

        return render(request, 'home.html', context)
