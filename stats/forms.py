from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . models import Game

class AddGameDataForm(forms.ModelForm):
	secretKey = forms.CharField()

	class Meta:
		model = Game
		fields = ['player', 'opponent', 'gameMode', 'deckCode', 'regions', 'expeditionWins', 'expeditionLosses', 'win']

class AddReplayData(forms.Form):
	replay = forms.CharField()