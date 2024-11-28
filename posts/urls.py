from django.urls import path

from posts.views import PostListView, CreateView, DetailView, UpdateView, DeleteView, PostCommentView

app_name = 'posts'
urlpatterns = [
    path('list/', PostListView.as_view(), name='list'),
    path('create/', CreateView.as_view(), name='create'),
    path('<int:pk>/', DetailView.as_view(), name="detail"),
    path('<int:pk>/comment/', PostCommentView.as_view(), name="comment"),
    path('<int:pk>/update/', UpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', DeleteView.as_view(), name='delete'),

]