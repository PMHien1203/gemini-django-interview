from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from .models import UserProfile

def register_view(request):
    if request.user.is_authenticated:
        return redirect('progress:dashboard')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            profile = user.profile
            profile.target_role = form.cleaned_data['target_role']
            profile.experience_level = form.cleaned_data['experience_level']
            profile.save()

            login(request, user)
            profile.update_streak()
            messages.success(request, f"Welcome to Python & Django Interview Master, {user.username}!")
            return redirect('progress:dashboard')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('progress:dashboard')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if hasattr(user, 'profile'):
                user.profile.update_streak()
            messages.success(request, f"Welcome back, {user.username}!")
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('progress:dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')

def demo_login_view(request):
    """Instantly logs in or provisions a demo candidate account for instant evaluation."""
    demo_user, created = User.objects.get_or_create(
        username='demo_developer',
        defaults={
            'email': 'developer@interviewmaster.io',
            'first_name': 'Alex',
            'last_name': 'Rivera',
        }
    )
    if created:
        demo_user.set_password('DjangoPython2026!')
        demo_user.save()
        demo_user.profile.target_role = 'senior'
        demo_user.profile.experience_level = 'ADVANCED'
        demo_user.profile.bio = 'Python and Django backend engineer preparing for staff-level interview loops.'
        demo_user.profile.save()
    
    login(request, demo_user)
    demo_user.profile.update_streak()
    messages.success(request, "Logged in as Demo Developer (Alex Rivera). Explore the dashboard, questions, and quizzes!")
    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('progress:dashboard')

@login_required
def profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('accounts:profile')
    else:
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        form = UserProfileForm(instance=profile, initial=initial_data)

    return render(request, 'accounts/profile.html', {
        'form': form,
        'profile': profile,
    })

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
            return redirect('accounts:profile')
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})
