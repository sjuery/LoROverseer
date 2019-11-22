import io
import json
import os
import requests
from lor_deckcodes import LoRDeck
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.files.storage import default_storage as storage
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from . forms import AddGameDataForm, AddReplayData
from . models import Game, Region, Deck, Card
from users.models import Profile

def Overall(request):
    totalGames = 0

    for region in Region.objects.all():
        totalGames += region.normalTotal + region.expeditionTotal
    return render(request, 'stats/overall.html', {'regions': Region.objects.all(), 'totalGames':totalGames})

def Normal(request):
    totalGames = 0

    for region in Region.objects.all():
        totalGames += region.normalTotal
    return render(request, 'stats/normal.html', {'regions': Region.objects.all(), 'totalGames':totalGames})

def Expedition(request):
    totalGames = 0

    for region in Region.objects.all():
        totalGames += region.expeditionTotal
    return render(request, 'stats/expedition.html', {'regions': Region.objects.all(), 'totalGames':totalGames})

def UpdateStats(requests):
    for game in Game.objects.all():
        unpackedDeck = LoRDeck.from_deckcode(game.deckCode)
        for card in list(unpackedDeck):
            try:
                newCard = Card.objects.get(id=card[2:])
                if game.gameMode == 'Normal':
                    if game.win:
                        newCard.normalWins += 1
                    newCard.normalTotal += 1
                else:
                    if game.win:
                        newCard.expeditionWins += 1
                    newCard.expeditionTotal += 1
            except:
                if game.win:
                    if game.gameMode == 'Normal':
                        newCard = Card(id=card[2:], normalWins=1, normalTotal=1, expeditionWins=0, expeditionTotal=0)
                    else:
                        newCard = Card(id=card[2:], normalWins=0, normalTotal=0, expeditionWins=1, expeditionTotal=1)
                else:
                    if game.gameMode == 'Normal':
                        newCard = Card(id=card[2:], normalWins=0, normalTotal=1, expeditionWins=0, expeditionTotal=0)
                    else:
                        newCard = Card(id=card[2:], normalWins=0, normalTotal=0, expeditionWins=0, expeditionTotal=1)
            newCard.save()

def Cards(request):
    demaciaNormal, demaciaExpedition, freljordNormal, freljordExpedition, ioniaNormal, ioniaExpedition, noxusNormal, noxusExpedition, pazNormal, pazExpedition, shadowNormal, shadowExpedition = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    for region in Region.objects.all():
        if "Demacia" in region.name:
            demaciaNormal += region.normalTotal
            demaciaExpedition += region.expeditionTotal
        if "Freljord" in region.name:
            freljordNormal += region.normalTotal
            freljordExpedition += region.expeditionTotal
        if "Ionia" in region.name:
            ioniaNormal += region.normalTotal
            ioniaExpedition += region.expeditionTotal
        if "Noxus" in region.name:
            noxusNormal += region.normalTotal
            noxusExpedition += region.expeditionTotal
        if "Piltover & Zaun" in region.name:
            pazNormal += region.normalTotal
            pazExpedition += region.expeditionTotal
        if "Shadow Isles" in region.name:
            shadowNormal += region.normalTotal
            shadowExpedition += region.expeditionTotal
    return render(request, 'stats/cards.html', {'cards': Card.objects.all(), 'demaciaNormal': demaciaNormal, 'demaciaExpedition': demaciaExpedition, 'freljordNormal': freljordNormal, 'freljordExpedition': freljordExpedition, 'ioniaNormal': ioniaNormal, 'ioniaExpedition': ioniaExpedition, 'noxusNormal': noxusNormal, 'noxusExpedition': noxusExpedition, 'pazNormal': pazNormal, 'pazExpedition': pazExpedition, 'shadowNormal': shadowNormal, 'shadowExpedition': shadowExpedition})

def NormalDecks(request):
    allDecksTotal = 0

    for deck in Deck.objects.all():
        allDecksTotal += deck.totalGames
    return render(request, 'stats/decksNormal.html', {'decks': Deck.objects.all().order_by('-totalGames'), 'allDecksTotal': allDecksTotal})

class UserGameListView(ListView):
    model = Game
    template_name = 'stats/profileGames.html'
    context_object_name = 'games'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        return Game.objects.filter(user=user).order_by('-datePlayed')

@csrf_exempt
def AddData(request):
    if request.method == 'POST':
        dataForm = AddGameDataForm(request.POST)
        replayForm = AddReplayData(request.POST)
        print(dataForm.errors)
        if dataForm.is_valid() and replayForm.is_valid():
            username = dataForm.cleaned_data.get('player')
            replay = replayForm.cleaned_data.get('replay')
            secretKey = dataForm.cleaned_data.get('secretKey')
            win = dataForm.cleaned_data.get('win')
            gameMode = dataForm.cleaned_data.get('gameMode')
            data = json.loads(replay)
            dataForm.instance.user = Profile.objects.get(secretKey=secretKey).user
            newPost = dataForm.save()
            #Region
            try:
                region = Region.objects.get(name=newPost.regions)
                if gameMode == 'Normal':
                    if win:
                        region.normalWins += 1
                    region.normalTotal += 1
                else:
                    if win:
                        region.expeditionWins += 1
                    region.expeditionTotal += 1
            except:
                if win:
                    if gameMode == 'Normal':
                        region = Region(name=newPost.regions, normalWins=1, normalTotal=1, expeditionWins=0, expeditionTotal=0)
                    else:
                        region = Region(name=newPost.regions, normalWins=0, normalTotal=0, expeditionWins=1, expeditionTotal=1)
                else:
                    if gameMode == 'Normal':
                        region = Region(name=newPost.regions, normalWins=0, normalTotal=1, expeditionWins=0, expeditionTotal=0)
                    else:
                        region = Region(name=newPost.regions, normalWins=0, normalTotal=0, expeditionWins=0, expeditionTotal=1)
            region.save()
            #Decks
            if gameMode == 'Normal':
                try:
                    deck = Deck.objects.get(code=newPost.deckCode)
                    if win:
                        deck.wins += 1
                    deck.totalGames += 1
                except:
                    if win:
                        deck = Deck(code=newPost.deckCode, wins=1, totalGames=1, regions=newPost.regions)
                    else:
                        deck = Deck(code=newPost.deckCode, wins=0, totalGames=1, regions=newPost.regions)
                deck.save()
            #Cards
            unpackedDeck = LoRDeck.from_deckcode(newPost.deckCode)
            for card in list(unpackedDeck):
                try:
                    newCard = Card.objects.get(id=card[2:])
                    if gameMode == 'Normal':
                        if win:
                            newCard.normalWins += 1
                        newCard.normalTotal += 1
                    else:
                        if win:
                            newCard.expeditionWins += 1
                        newCard.expeditionTotal += 1
                except:
                    if win:
                        if gameMode == 'Normal':
                            newCard = Card(id=card[2:], normalWins=1, totalWins=1, expeditionWins=0, expeditionTotal=0)
                        else:
                            newCard = Card(id=card[2:], normalWins=0, totalWins=0, expeditionWins=1, expeditionTotal=1)
                    else:
                        if gameMode == 'Normal':
                            newCard = Card(id=card[2:], normalWins=0, normalTotal=1, expeditionWins=0, expeditionTotal=0)
                        else:
                            newCard = Card(id=card[2:], normalWins=0, normalTotal=0, expeditionWins=0, expeditionTotal=1)
                newCard.save()
            with storage.open(f'replayData/{newPost.pk}.json', 'w') as f:
                json.dump(data, f)
            return redirect('profileGames')
    else:
        dataForm = AddGameDataForm()
        replayForm = AddReplayData()
    return render(request, 'stats/addGame.html', {'dataForm':dataForm, 'replayForm':replayForm})

@csrf_exempt
def Replay(request, pk, fn):
    with storage.open(f'replayData/{pk}.json', 'r') as f:
        jsonData = json.load(f)
    cards = jsonData['frame' + str(fn)]
    if 'frame' + str(fn+1) in jsonData:
        nextPage = fn+1
    else:
        nextPage = 0
    if 'frame' + str(fn-1) in jsonData:
        previousPage = fn-1
    else:
        previousPage = 0
    return render(request, 'stats/replay.html', {'cards':cards, 'nextPage':nextPage, 'previousPage':previousPage})

def About(request):
    return render(request, 'stats/about.html', {'title': 'About'})
