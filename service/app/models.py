from django.db import models

# Create your models here.


class User(models.Model):

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(primary_key=True, max_length=100, blank=False)
    password = models.CharField(max_length=255, blank=False)
    avatar = models.CharField(max_length=1024)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.username
