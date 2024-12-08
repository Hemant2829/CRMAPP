from django.shortcuts import render,redirect
from .forms import CreateUserForm, LoginForm, CreateRecordForm, UpdateRecordForm,crispy_forms
from .models import Record
from django.contrib.auth.models import auth
from django.contrib.auth  import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def home(request):

    return render(request, 'crmapp/index.html')


def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Account Created Succesfully!")
        
            return redirect('my-login')
   
    return render(request, 'crmapp/register.html', {'form':form})


def my_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password) 
            if user is not None:
                auth.login(request,user)
                messages.success(request,"Your Login  Succesfully!")
                return redirect('dashboard')
    context = {'form':form}
    return render(request,'crmapp/my-login.html',context=context)

# - User Logout
def user_logout(request):
    auth.logout(request)
    messages.success(request," Logout Success!")
    return redirect("my-login")
 
@login_required(login_url='my-login')
def dashboard(request):
    my_records = Record.objects.all()
    context = {'records': my_records}
    return render(request, 'crmapp/dashboard.html', context=context)


@login_required(login_url='my-login')
def create_record(request):
    form = CreateRecordForm()
    if request.method == 'POST':
        form =CreateRecordForm(request.POST)
        if form.is_valid:
            form.save()
            messages.success(request,"Your record was created !")
            return redirect("dashboard")
    
    context = {'form':form}
    return render(request,'crmapp/create-record.html',context=context )

def customer_record(request,pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, 'crmapp/view-record.html',{'customer_record': customer_record})
    else :
        return redirect('home')
@login_required(login_url='my-login')
def delete_record(request, pk):
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request,"Delete Succesfully!")
        return redirect("dashboard")

def update_record(request,pk):
    record = Record.objects.get(id=pk)
    form = UpdateRecordForm(instance=record)
    if request.method == 'POST':
        form = UpdateRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request,"Your record was updated !")
            return redirect("dashboard")
    return render(request,'crmapp/update-record.html',{'form':form})

    




    

        
