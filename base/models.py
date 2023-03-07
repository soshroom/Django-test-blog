from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class like:
    def number_of_likes(self):
        return self.likes.count()

    def isLiked(self, user: User):
        if user.is_anonymous:
            return False
        return self.likes.contains(user)

    def like(self, user: User):
        if not self.likes.contains(user):
            self.likes.add(user)
        else:
            self.likes.remove(user)


class Post(models.Model, like):
    name = models.CharField(max_length=80)
    content = models.TextField(max_length=512)
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    likes = models.ManyToManyField(User, related_name="post_like")
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.name


class Comment(models.Model, like):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name="comment_like")
    content = models.TextField(max_length=512)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']
