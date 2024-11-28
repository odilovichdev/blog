from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from blog import settings
from posts.views import AdminPostApprovalView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('posts/', include('posts.urls')),
    path('', include('common.urls')),
    path('approval/', AdminPostApprovalView.as_view(), name='admin_approval'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
