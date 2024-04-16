from django.shortcuts import redirect,render
from django.contrib.auth.models import User
from django.contrib import messages
from app.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate,login,logout

def REGISTER(request):
    email = None
    password = None
    username = None
    if request.method == "POST":
       username = request.POST.get('username')
       email = request.POST.get('email')
       password = request.POST.get('password')
    #    print(username,email,password)
       #    check username
       if User.objects.filter(email=email).exists():
           messages.warning(request,'Email are Already Exists !')
           return redirect('register')
       # check username
       if User.objects.filter(username=username).exists():
           messages.warning(request,'Username are Already exists !')
           return redirect('register')

       user = User (
          username=username,
          email=email,
        )
       user.set_password(password)
       user.save()
       return redirect('login')
    return render(request,'registration/register.html')

def Do_LOGIN(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = EmailBackEnd.authenticate(request,
                                         username=email,
                                         password=password)
        
        if user != None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Email and Password Are Invalid !')
            return redirect('login')
    
def PROFILE(request):
    return render(request,'registration/profile.html')
    return None