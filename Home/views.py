from django.shortcuts import render, HttpResponse, redirect
from .models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from Blog.models import Blog
import re


# HTML pages.
def home(request):
    return render(request, "home/home.html")

def about(request):
    return render(request, "home/about.html")

def search(request):
    query = request.GET["query"]
    if len(query) > 70:
        query = query[:70]
    postsTitle = Blog.objects.filter(title__icontains = query)
    postsContent = Blog.objects.filter(content__icontains = query)
    postsAuthor = Blog.objects.filter(author__icontains = query)
    posts = postsTitle.union(postsContent, postsAuthor)
    if len(posts) == 0:
        messages.warning(request, "No Search results, Please refine your request!")
        params = {"posts":posts, "find":False, "query":query}
        return render(request, "home/search.html", context={'params': params})

    else:
        params = {"posts":posts, "find":True, "query":query}
        return render(request, "home/search.html", params)
    


# Authentication routes
def handleSignup(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        terms = request.POST.get("terms")

        if not is_valid_email(email) or not is_valid_name(username) or not is_valid_password(password1) or not is_valid_password(password2) or password1 != password2:
                messages.warning(request, "Account was not created, given data is not valid, Try again!")
                return redirect("/")

        myUser = User.objects.create_user(username, email, password1)
        myUser.first_name = fname
        myUser.last_name = lname
        myUser.save()
        messages.success(request, "Your iCoder account has been successfully created!")
        return redirect("/")
    else:
        return HttpResponse("<h1>Error 404 - Page not found.</h1>")

def handleLogin(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in!")
            return redirect("/")
        
        else:
            messages.error(request, "No data found in Records!")
            return redirect("/")

def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully logout!")
    return redirect("/")





# Other endpoints.
def contact(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        contact = request.POST.get("contact")
        email = request.POST.get("email")
        password = request.POST.get("password")
        message = request.POST.get("message")

        if is_valid_email(email) and is_valid_name(name) and is_valid_password(password) and is_valid_phone_number(contact):
            contact = Contact(name = name, contact = contact, email = email, password=password, message = message)
            contact.save()
            messages.success(request, "Successfully submitted the Form.")
        else:
            messages.error(request, "Alert, One or more details are not Valid.")
    return render(request, "home/contact.html")

def is_valid_email(email):
     # Define the regular expression pattern for a valid email
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    # Use re.match() to check if the email matches the pattern
    match = re.match(pattern, email)
    # Return True if the email is valid, otherwise False
    return bool(match)

def is_valid_name(name):
    # Name should contain only letters and spaces
    return bool(re.match(r'^[a-zA-Z\s]+$', name))

def is_valid_phone_number(phone_number):
    # Phone number should contain only digits and be 10 digits long
    return bool(re.match(r'^\d{10}$', phone_number))

def is_valid_password(password):
    # Password should be at least 8 characters long, containing letters, digits, and special characters
    return bool(re.match(r'^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password))

