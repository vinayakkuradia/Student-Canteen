from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.messages import info
from mess.admin import UserCreationForm

# Create your views here.
def home(request):
    return render(request, 'mess/home.html')

def login(request):
    if request.method == 'POST':
        mobile = request.POST['mobile']
        password = request.POST['password']

        user = auth.authenticate(mobile=mobile, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            info(request, 'invalid credentials')
            return redirect('home')

    else:
        return redirect('home')

def logout(request):
    auth.logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('home')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            mobile = form.cleaned_data['mobile']
            password = form.cleaned_data['password1']
            user = auth.authenticate(mobile=mobile, password=password)
            auth.login(request, user)
            return redirect('home')
        else:
            redirect('signup')
    else:
        form = UserCreationForm()

    context = {'form' : form}
    return render(request, 'mess/signup.html', context)