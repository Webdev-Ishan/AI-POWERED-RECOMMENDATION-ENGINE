from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.http import JsonResponse
from .forms import UserForm, ProfileForm
from .models import Profile
from django.views.decorators.csrf import csrf_exempt  # Import the decorator
from django.contrib.auth.decorators import login_required
import json


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
            auth_login(request, user)

            return JsonResponse({"message": "User and Profile created successfully"}, status=201)

        # If forms are not valid, return errors
        return JsonResponse({"errors": user_form.errors | profile_form.errors}, status=400)
    
    else:
        # Handle GET request (return empty forms)
        user_form = UserForm()
        profile_form = ProfileForm()

    return render(request, 'your_template.html', {'user_form': user_form, 'profile_form': profile_form})

@csrf_exempt
@login_required
def profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    return JsonResponse({
        'username': user.username,
        'email': user.email,
        'profile_pic': profile.profilepic.url if profile.profilepic else None,
        'created_at': profile.created_at,
    }, status=200)

@csrf_exempt
def login_view(request):
    if request.method == "POST":
     try:     
        data = json.loads(request.body) # to convert thwe json body of postman into dictionary

        username = data.get('username')
        password = data.get('password')
        print(username)
        print(password)
        if not username or not password:
            return JsonResponse({"error": "User not found "}, status=404)
        user = authenticate(request,username=username,password=password)

        if user is not None:
            auth_login(request, user)
            return JsonResponse({'message': 'Login successful', 'username': user.username}, status=200)

        else:
          return JsonResponse({'error': 'Invalid credentials'}, status=401)
    

     except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
