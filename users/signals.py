from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from . models import Profile
import secrets

@receiver(post_save, sender=User)
def CreateProfile(sender, instance, created, **kwargs):
	secretKey = secrets.token_hex(16)
	if created:
		Profile.objects.create(user=instance, secretKey=secretKey)

@receiver(post_save, sender=User)
def SaveProfile(sender, instance, **kwargs):
	instance.profile.save()