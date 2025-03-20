from tkinter.constants import CASCADE

from django.db import models
from django.urls import reverse

# Create your models here.
from django.contrib.auth.models import User
from django.utils import timezone
class Post(models.Model):
	title=models.CharField(max_length=200)
	content=models.TextField()
	date_posted=models.DateTimeField(default=timezone.now)
	author=models.ForeignKey(User,on_delete=models.CASCADE)

	def __str__(self):
		return self.title
	def get_absolute_url(self):
		return reverse('blog-detail',kwargs={'pk':self.pk})

class Comment(models.Model):
	blog=models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE)
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	content=models.TextField()
	date_created=models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f'Comment by {self.user.username} on {self.blog.title}'

