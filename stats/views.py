import io
import json
import os
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from . forms import AddGameDataForm, AddReplayData
from . models import Game

def Home(request):
    return render(request, 'stats/home.html', {'games': Game.objects.all()})

class StatsListView(ListView):
    model = Game
    template_name = 'stats/home.html'
    context_object_name = 'games'
    ordering = ['-datePlayed']
    paginate_by = 5

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

class StatsCreateView(LoginRequiredMixin, CreateView):
    model = Game
    fields = ['player', 'opponent']
    template_name = 'stats/gameCreate.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class StatsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Game
    fields = ['player', 'opponent']
    template_name = 'stats/gameCreate.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        game = self.get_object()
        if self.request.user == game.user:
            return True
        return True

class StatsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Game
    template_name = 'stats/gameDelete.html'
    context_object_name = 'game'
    success_url = '/'
    
    def test_func(self):
        game = self.get_object()
        if self.request.user == game.user:
            return True
        return True

@csrf_exempt
def AddData(request):
    if request.method == 'POST':
        dataForm = AddGameDataForm(request.POST)
        replayForm = AddReplayData(request.POST)
        if dataForm.is_valid() and replayForm.is_valid():
            username = dataForm.cleaned_data.get('player')
            replay = replayForm.cleaned_data.get('replay')
            data = json.loads(replay)
            newPost = dataForm.save()
            with open(f'replayData/{newPost.pk}.json', 'w') as f:
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
