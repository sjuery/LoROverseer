from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from . models import Profile
import secrets

@receiver(post_save, sender=User)
def CreateProfile(sender, instance, created, **kwargs):
	secretCode = secrets.token_hex(16)
	while Profile.objects.filter(secretCode=secretCode) != None:
		secretCode = secrets.token_hex(16)
	Profile.secretCode = secretCode
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def SaveProfile(sender, instance, **kwargs):
	instance.profile.save()