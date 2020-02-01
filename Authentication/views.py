from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpadateForm, ProfileUpdateForm
from django.contrib import messages




# Create your views here.

#function for signup
'''def signup_view(request):
	if request.method=='POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request,user)
			return redirect('')

	else:
		form = UserCreationForm()

	return render(request, 'Authentication/signup_view.html',{'form':form})'''
@login_required
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your Account has been created for {username}! You are now able to login')
            

    else:
        form = UserRegisterForm()
    return render(request,'Authentication/register.html',{'form':form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpadateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid:
            u_form.save()
            p_form.save()
            username = u_form.cleaned_data.get('username')
            messages.success(request, f'{username}, Your acoount has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpadateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request,'Authentication/profile.html',context)





#function for login
def login_view(request):
	if request.method=='POST':
		print(request.POST['username'])
		form = authenticate(username=request.POST['username'], password=request.POST['pass'])
		if form is not None:
			user = form
			login(request,user)
			return redirect('Process:homepage')

	'''else:
		form = AuthenticationForm()'''

	return render(request, 'Authentication/login_view.html')


#function for logout
def logout_view(request):
	if request.method=='POST':
		logout(request)
		return redirect('Authentication:login')

