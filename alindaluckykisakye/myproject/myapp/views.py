from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import re
from .models import CustomUser 


def is_valid_format(input_string, pattern):
    """Checks if the input string matches a given regex pattern."""
    return bool(re.match(pattern, input_string))

# --- Django Views ---

def login_view(request):
    """Handles user login using Django's built-in authentication."""
    context = {
        'username_class': '',
        'password_class': '',
        'username_value': '',
        'message': '',
    }

    if request.method == 'POST':
        username = request.POST.get('username', '').strip() 
        password = request.POST.get('password', '')
        
        context['username_value'] = username

        # Attempt to authenticate the user (using email as username)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # --- SUCCESSFUL LOGIN ---
            login(request, user)
            # Use full_name for a personalized message
            name = user.full_name.split()[0] if user.full_name else user.username 
            messages.success(request, f"Welcome back, {name}!")
            return redirect(reverse('dashboard'))
        else:
            # --- FAILED AUTHENTICATION ---
            messages.error(request, "Error: Invalid email or password.")
            context['username_class'] = 'is-invalid'
            context['password_class'] = 'is-invalid'
    
    # If it was a GET request or authentication failed, render the login page
    return render(request, 'login.html', context)


def signup_view(request):
    """Handles user registration with detailed field validation feedback."""
    # Initialize context with default classes (empty) and placeholder values
    context = {
        'full_name_class': '', 'email_class': '', 'phone_number_class': '',
        'password_class': '', 'confirm_password_class': '',
        'full_name_value': '', 'email_value': '', 'phone_number_value': '',
    }

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '')
        email = request.POST.get('email', '')
        phone_number = request.POST.get('phone_number', '')
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        
        
        context.update({
            'full_name_value': full_name, 
            'email_value': email, 
            'phone_number_value': phone_number,
        })
        
        is_form_valid = True
        
        # --- Validation and Class Assignment ---

        # Full Name Check (must not be too short)
        if len(full_name) < 3:
            messages.error(request, "Full name must be at least 3 characters.")
            context['full_name_class'] = 'is-invalid'
            is_form_valid = False
        else:
            context['full_name_class'] = 'is-valid'

        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not is_valid_format(email, email_pattern):
            messages.error(request, "Invalid email format.")
            context['email_class'] = 'is-invalid'
            is_form_valid = False
        elif CustomUser.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered.")
            context['email_class'] = 'is-invalid'
            is_form_valid = False
        else:
            context['email_class'] = 'is-valid'

        if len(phone_number) != 10 or not phone_number.isdigit():
            messages.error(request, "Phone number must be exactly 10 digits (digits only).")
            context['phone_number_class'] = 'is-invalid'
            is_form_valid = False
        elif CustomUser.objects.filter(phone_number=phone_number).exists():
            messages.error(request, "This phone number is already registered.")
            context['phone_number_class'] = 'is-invalid'
            is_form_valid = False
        else:
            context['phone_number_class'] = 'is-valid'
        
        
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters.")
            context['password_class'] = 'is-invalid'
            context['confirm_password_class'] = 'is-invalid'
            is_form_valid = False
        elif password != confirm_password:
            messages.error(request, "Passwords do not match.")
            context['password_class'] = 'is-invalid'
            context['confirm_password_class'] = 'is-invalid'
            is_form_valid = False
        else:
            context['password_class'] = 'is-valid'
            context['confirm_password_class'] = 'is-valid'
            

        if not is_form_valid:
            
            return render(request, 'signup.html', context)

        # 3. Create User (Only if validation passed)
        try:
            
            user = CustomUser.objects.create_user(
                username=email, 
                email=email,
                password=password,
                full_name=full_name,
                phone_number=phone_number
            )
            user.save()
            
            # --- SUCCESS REDIRECT: Changed from 'login' to 'success' ---
            
            return redirect('success') 
        
        except Exception as e:
            messages.error(request, f"An unexpected server error occurred during signup: {e}")
            return render(request, 'signup.html', context)

    #
    return render(request, 'signup.html', context)

# --- NEW VIEW: success_view ---
def success_view(request):
    """Renders the congratulatory page after a successful action (e.g., sign-up)."""
   
    return render(request, 'success.html')


@login_required(login_url='login')
def dashboard_view(request):
    """Protected view only accessible to logged-in users."""
    return render(request, 'dashboard.html', {})

def user_logout(request):
    """Logs the user out."""
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')
