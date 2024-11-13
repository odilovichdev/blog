from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel
from users.models import CustomUser


class Post(BaseModel):
    class Status(models.TextChoices):
        DRAFT = "DB", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(_("Title"), max_length=250)
    desc = models.TextField(_("Desc"))
    image = models.ImageField(upload_to="posts/", default="posts/default-post.jpeg")
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    view_count = models.PositiveIntegerField(default=0)
    is_recommended = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class PostView(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='post_views')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f"{self.post.title} by {self.user.first_name}"


class Comment(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField(_("Text"))

    def __str__(self):
        return f"{self.user.first_name} by comment"
