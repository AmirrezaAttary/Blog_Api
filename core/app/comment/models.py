from django.db import models
from django.urls import reverse
from ..blog.models import Post

# Create your models here.
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="post_comment")
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    approved = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_date']
    
    def __str__(self):
        return self.name
    
    def get_absolute_api_url(self):
        return reverse("comment:api-v1:comment-detail", kwargs={"pk": self.pk})