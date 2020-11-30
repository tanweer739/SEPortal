from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm,ProfileUpdateForm


# Create your views here.

@login_required  # decoreates add functionalites to existing fucntionalities
def profile(request):
    if request.method == 'POST':
        #gets the form with data in it to these variables
        userform = UserUpdateForm(request.POST, instance=request.user)
        profileform = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if userform.is_valid() and profileform.is_valid():
            userform.save()
            profileform.save()
            messages.success(request, 'Your account has been updated ')
            return redirect('profile')
    else:
        #while viewing the profile page fields are populated with current instances
        userform = UserUpdateForm(instance=request.user)
        profileform = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'userform': userform,
        'profileform': profileform
    }
    return render(request, 'users/profile.html', context)
