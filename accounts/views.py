from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def register_view(request):
    #if form is submit 
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get(password)
        cpassword = request.POST.get(cpass)
        if password != cpassword or len(password) > 0 or len(cpassword) > 0:
            messages.error( request,"passwords do not match")
            return redirect('register')
        #user create
        #user create karo
        user = user.objects.create_user (username, email, password)
        messages.success (request, "Account created succesfully")
        return redirect('login')
    else:
        return render(request, 'accounts/register.html')
    
def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        if len(email) == 0 or len (password) == 0:
            messages.error(request, "Invalid credentials")
            return redirect ('login')
        # user authenticate karo
        user = authenticate (request, email=email, password=password)
        if user is not None:
            messages.success(request, "Loggout in successfully")
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')
    
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect( 'login')

def profile_view(request):
    return render(request, ' accounts/profile.html')



