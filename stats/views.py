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

def Cards(request):
    r = requests.get("https://lor.mln.cx/Set1/en_us/data/set1-en_us.json")
    data = r.json()
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

class UserGameListView(ListView):
    model = Game
    template_name = 'stats/profileGames.html'
    context_object_name = 'games'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        return Game.objects.filter(user=user).order_by('-datePlayed')

class StatsDetailView(DetailView):
    model = Game
    template_name = 'stats/gameDetails.html'
    context_object_name = 'game'

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
                        region = Region(name=newPost.regions, normalWins=1, totalWins=1, expeditionWins=0, expeditionTotal=0)
                    else:
                        region = Region(name=newPost.regions, normalWins=0, totalWins=0, expeditionWins=1, expeditionTotal=1)
            region.save()
            #Decks
            try:
                deck = Deck.objects.get(code=newPost.deckCode)
                if win:
                    deck.wins += 1
                deck.totalGames += 1
            except:
                if win:
                    deck = Deck(code=newPost.deckCode, wins=1, totalGames=1)
                else:
                    deck = Deck(code=newPost.deckCode, wins=0, totalGames=1)
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
                newCard.save()
            with storage.open(f'replayData/{newPost.pk}.json', 'w') as f:
                json.dump(data, f)
            return redirect('profileGames')
    else:
        dataForm = AddGameDataForm()
        replayForm = AddReplayData()
    return render(request, 'stats/addGame.html', {'dataForm':dataForm, 'replayForm':replayForm})

@csrf_exempt
def Replay(request):
	cards = [{"CardID":224603010,"CardCode":"face","TopLeftX":179,"TopLeftY":716,"Width":117,"Height":117,"LocalPlayer":False},{"CardID":56783077,"CardCode":"face","TopLeftX":179,"TopLeftY":481,"Width":117,"Height":117,"LocalPlayer":True},{"CardID":1856610393,"CardCode":"01SI049","TopLeftX":518,"TopLeftY":69,"Width":194,"Height":306,"LocalPlayer":True},{"CardID":175243887,"CardCode":"01FR009","TopLeftX":896,"TopLeftY":980,"Width":127,"Height":160,"LocalPlayer":False},{"CardID":1727472316,"CardCode":"01SI042","TopLeftX":375,"TopLeftY":450,"Width":176,"Height":158,"LocalPlayer":True},{"CardID":1868163728,"CardCode":"01SI023","TopLeftX":896,"TopLeftY":260,"Width":127,"Height":160,"LocalPlayer":True},{"CardID":337837419,"CardCode":"01SI047","TopLeftX":689,"TopLeftY":76,"Width":195,"Height":308,"LocalPlayer":True},{"CardID":1328058304,"CardCode":"01NX032","TopLeftX":739,"TopLeftY":980,"Width":127,"Height":160,"LocalPlayer":False},{"CardID":1251836690,"CardCode":"01NX032","TopLeftX":1052,"TopLeftY":980,"Width":127,"Height":160,"LocalPlayer":False},{"CardID":1523096865,"CardCode":"01SI049","TopLeftX":861,"TopLeftY":76,"Width":196,"Height":309,"LocalPlayer":True},{"CardID":1459407373,"CardCode":"01SI034","TopLeftX":1035,"TopLeftY":71,"Width":197,"Height":310,"LocalPlayer":True},{"CardID":1860326221,"CardCode":"01SI021","TopLeftX":1211,"TopLeftY":59,"Width":198,"Height":312,"LocalPlayer":True},{"CardID":1709056436,"CardCode":"01SI007T1","TopLeftX":573,"TopLeftY":450,"Width":176,"Height":158,"LocalPlayer":True},{"CardID":440628488,"CardCode":"01SI007T1","TopLeftX":772,"TopLeftY":450,"Width":176,"Height":158,"LocalPlayer":True},{"CardID":976729633,"CardCode":"01SI007T1","TopLeftX":970,"TopLeftY":450,"Width":176,"Height":158,"LocalPlayer":True},{"CardID":2098056557,"CardCode":"01SI024","TopLeftX":1169,"TopLeftY":450,"Width":176,"Height":158,"LocalPlayer":True},{"CardID":2028932613,"CardCode":"01SI024","TopLeftX":1367,"TopLeftY":450,"Width":176,"Height":158,"LocalPlayer":True}]
	return render(request, 'stats/replay.html', {'cards':cards})

def About(request):
    return render(request, 'stats/about.html', {'title': 'About'})
