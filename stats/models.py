from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Game(models.Model):
	player = models.CharField(max_length=25)
	opponent = models.CharField(max_length=25)
	deckCode = models.CharField(max_length=100)
	gameMode = models.CharField(max_length=11, default='Normal')
	regions = models.CharField(max_length=100)
	expeditionWins = models.IntegerField(default=0)
	expeditionLosses = models.IntegerField(default=0)
	win = models.BooleanField()
	datePlayed = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
	
	def __str__(self):
		return self.player + " VS " + self.opponent
	
	def get_absolute_url(self):
		return reverse('gameDetails', kwargs={'pk': self.pk})

class Region(models.Model):
	name = models.CharField(max_length=100, unique=True, primary_key=True)
	wins = models.IntegerField()
	losses = models.IntegerField()
	totalGames = models.IntegerField()
    
	def __str__(self):
		return self.name

class Deck(models.Model):
	code = models.CharField(max_length=50, unique=True, primary_key=True)
	wins = models.IntegerField()
	losses = models.IntegerField()
	totalGames = models.IntegerField()
    
	def __str__(self):
		return self.code

class Card(models.Model):
	id = models.CharField(max_length=10, unique=True, primary_key=True)
	wins = models.IntegerField()
	losses = models.IntegerField()
	totalGames = models.IntegerField()
    
	def __str__(self):
		return self.id
