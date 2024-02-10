from django.db import models

# Create your models here.
class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=70, default="")
    email = models.EmailField(max_length=100, default="")
    password = models.CharField(max_length=20, default="")
    contact = models.IntegerField(default=0)
    timestamp = models.TimeField(auto_now_add=True)
    message = models.TextField(max_length=500, default="")

    def __str__(self):
        return "Message from " + self.name + " - " + self.email