from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

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
		profileForm = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		if userForm.is_valid() and profileForm.is_valid():
			userForm.save()
			profileForm.save()
			username = userForm.cleaned_data.get('username')
			messages.success(request, f'Account for {username} successfully updated.')
			return redirect('profile')
	else:
		userForm = UserUpdateForm(instance=request.user)
		profileForm = ProfileUpdateForm()
	return render(request, 'users/profile.html', {'userForm':userForm, 'profileForm':profileForm})