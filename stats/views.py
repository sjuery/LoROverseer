from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
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
        return False

class StatsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Game
    template_name = 'stats/gameDelete.html'
    context_object_name = 'game'
    success_url = '/'
    
    def test_func(self):
        game = self.get_object()
        if self.request.user == game.user:
            return True
        return False

def About(request):
    return render(request, 'stats/about.html', {'title': 'About'})
