from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . models import Game

class AddGameDataForm(forms.ModelForm):
	class Meta:
		model = Game
		fields = ['player', 'opponent', 'deckCode', 'win']