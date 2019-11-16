import secrets
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . forms import UserRegisterForm, UserUpdateForm
from . models import Profile

def Register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Account for {username} created successfully.')
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request, 'users/register.html', {'form':form})

@login_required
def Profile(request):
	if request.method == 'POST':
		userForm = UserUpdateForm(request.POST, instance=request.user)
		if userForm.is_valid():
			userForm.save()
			username = userForm.cleaned_data.get('username')
			messages.success(request, f'Account for {username} successfully updated.')
			return redirect('profile')
	else:
		userForm = UserUpdateForm(instance=request.user)
	return render(request, 'users/profile.html', {'userForm':userForm})