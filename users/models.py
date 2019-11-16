from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage as storage

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	secretKey = models.CharField(max_length=32)

	def __str__(self):
		return f'{self.user.username} Profile'

