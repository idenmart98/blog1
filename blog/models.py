from django.contrib.auth.models import User
from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    clipped_text = models.TextField(max_length=150)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    rating_sum = models.IntegerField(default=0)
    views = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.id} - {self.title}'


class Rate(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['owner', 'post']]


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f'{self.owner} - {self.post}'
