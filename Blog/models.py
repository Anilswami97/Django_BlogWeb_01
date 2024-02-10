from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.
class Blog(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=70)
    content = models.CharField(max_length=500)
    author = models.CharField(max_length=100)
    timestamp = models.DateField(blank=True)   
    
    def __str__(self):
        return "Name: "+self.author+" Title: "+self.title;
 
class BlogComment(models.Model):
    sno = models.AutoField(primary_key=True)
    Comment = models.CharField(max_length=10000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Blog, on_delete=models.CASCADE)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null = True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.Comment[0:13] + "... " + "by " + self.user.username
    