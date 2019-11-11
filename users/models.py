from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage as storage
from PIL import Image

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	picture = models.ImageField(default='profilePictures/default.jpg', upload_to='profilePictures')

	def __str__(self):
		return f'{self.user.username} Profile'

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		img_read = storage.open(self.picture.name, 'r')
		img = Image.open(img_read)

		if img.height > 128 or img.width > 128:
			output_size = (128, 128)
			img.thumbnail(output_size)
			in_mem_file = io.BytesIO()
			img.save(in_mem_file, format='JPEG')
			img_write = storage.open(self.picture.name, 'w+')
			img_write.write(in_mem_file.getvalue())
			img_write.close()

		img_read.close()

