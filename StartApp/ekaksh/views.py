
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from django.shortcuts import render, redirect
from .forms import DocumentForm
# views.py

from .models import UserProfile

def view_uploaded_files(request):
    # Query the database to retrieve the uploaded file records
    uploaded_files = UserProfile.objects.all()

    # Pass the retrieved records to a template
    return render(request, 'view_uploaded_files.html', {'uploaded_files': uploaded_files})

def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            if form.cleaned_data['upload_type'] == 'existing_folder':
                folder_name = form.cleaned_data['existing_folders']
            else:  # Create a new folder
                folder_name = form.cleaned_data['folder_name']  # Use provided folder name
            user_profile.document.name = 'user_{0}/{1}/{2}'.format(request.user.id, folder_name, form.cleaned_data['filename'])
            user_profile.save()
            return redirect('document_uploaded')
    else:
        form = DocumentForm(user=request.user)  # Pass user=request.user to the form
    return render(request, 'upload_document.html', {'form': form})




def home(request):
    return HttpResponse("All about Ekaksh with two functionality of login and sign up ")
def register(request):

    error_message = ""
    if request.method == "POST":
        
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            validate_email(email)
        except ValidationError:
            error_message = "Invalid email format. Please enter a valid email address."
            return HttpResponse(error_message)

        # Check if the username already exists
        user_exists =  user_exists = User.objects.filter(email=email).exists()

        if user_exists:
            error_message = "User already exists. Please choose a different email."
            return HttpResponse(error_message)
        else:
            # If username does not exist, create a new user
            user = User.objects.create(first_name=firstname, last_name=lastname, email=email)
            user.set_password(password)
            user.save()
            return HttpResponse("User registered successfully!")
    return HttpResponse("GET request received.")

def Login(request):

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the email is valid
        try:
            validate_email(email)
        except ValidationError:
            return HttpResponse("Invalid email format. Please enter a valid email address.")

        if not User.objects.filter(email=email).exists():
            return HttpResponse("Invalid email!")

        user = authenticate(request, email=email, password=password)

        if user is None:
            return HttpResponse("Invalid password!")
        else:
            login(request, user)
            return HttpResponse("Login successful!")

    return HttpResponse("GET request received.")

def LogOut(request):
    logout(request)
    return HttpResponse("Logged out successfully!")
