from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.messages import info
from mess.serializers import OrdersDataSerializer, OrdersAdminDataSerializer, OrdersSerializer
from django.contrib.auth.decorators import login_required

from mess.models import Order, Student
from mess.admin import UserCreationForm, OrderCreationForm

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

@login_required
def process_order(request):
    if request.method == 'POST':
        form = OrderCreationForm(request.POST)
        if form.is_valid():
            formdata = form.save(commit=False)
            formdata.ordered_by = Student.objects.get(mobile = request.user.mobile)
            formdata.save()
            info(request, 'Order placed successfully with Order ID: ' + str(formdata.order_id))
            return redirect('home')
        else:
            info(request, 'Something went wrong! Please try again..')
            return redirect('home')


@login_required
def myorders(request):
    if request.method == 'GET':
        if request.user.is_admin:
            queryresult = Order.objects.all().order_by('-datetime')
            serializer = OrdersSerializer(queryresult, many=True)
            data = serializer.data
            return render(request, 'mess/myorders.html', {'queryresult': data})
        else:
            queryresult = Order.objects.filter(ordered_by = (Student.objects.get(mobile=request.user.mobile))).order_by('-datetime')
            serializer = OrdersSerializer(queryresult, many=True)
            data = serializer.data
            return render(request, 'mess/myorders.html', {'queryresult': data})

