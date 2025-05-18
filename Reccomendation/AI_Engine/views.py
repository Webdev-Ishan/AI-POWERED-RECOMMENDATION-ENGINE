from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.http import JsonResponse
from .forms import UserForm, ProfileForm
from .models import Profile
from django.views.decorators.csrf import csrf_exempt  # Import the decorator
@csrf_exempt
def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        # Validate both forms
        if user_form.is_valid() and profile_form.is_valid():
            # Save user object
            user = user_form.save()

            # Save profile object with the user
            profile = profile_form.save(commit=False)
            profile.user = user  # Associate profile with the user
            profile.save()

            # Log the user in after successful registration
            login(request, user)

            return JsonResponse({"message": "User and Profile created successfully"}, status=201)

        # If forms are not valid, return errors
        return JsonResponse({"errors": user_form.errors | profile_form.errors}, status=400)
    
    else:
        # Handle GET request (return empty forms)
        user_form = UserForm()
        profile_form = ProfileForm()

    return render(request, 'your_template.html', {'user_form': user_form, 'profile_form': profile_form})
