from django.db import models

class AppUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=256)  # Will store hashed password
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username
