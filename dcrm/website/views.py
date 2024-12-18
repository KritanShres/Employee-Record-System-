from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Records
# Create your views here.

def home(request): 
    records = Records.objects.all()
    if request.method == "POST": 
        name  = request.POST['username']
        pw = request.POST['password']
        #authenticate 
        user = authenticate(request, username=name, password=pw)
        if user is not None: 
            login(request,user)
            messages.success(request, "You have been logged in") 
            return redirect('home')
        else: 
            messages.success(request, "There was an error loggin. Try again") 
            return redirect('home')
    else:
        return render(request, 'home.html',{'records':records}) 

def logout_user(request): 
    logout(request) 
    messages.success(request, "You have been logged out.") 
    return redirect('home') 
 

def register_user(request): 
    if request.method =="POST": 
        form = SignUpForm(request.POST)
        if form.is_valid(): 
            form.save() 
            username = form.cleaned_data['username'] 
            password = form.cleaned_data['password1']
            user = authenticate(username=username , password =password) 
            login(request, user) 
            messages.success(request, "You have successfully registered")
            return redirect('home')
    else: 
        form = SignUpForm()
        return render(request, 'register.html', {'form' : form})

    return render(request, 'register.html', {'form' : form})  


def customer_record(request, pk): 
    if request.user.is_authenticated: 
        customer_record = Records.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record' : customer_record}) 
    else: 
        messages.success(request, "You must be logged in to view records!")


def delete_record(request, pk): 
    if request.user.is_authenticated: 
        delete_it = Records.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, f"Record {delete_it} has been deleted" )
        return redirect('home')
    
    else: 
        messages.success(request, "You must be logged in to do that") 
        return redirect('home') 
    

def add_record(request):
    form = AddRecordForm(request.POST or None) 
    if request.user.is_authenticated: 
        if request.method =='POST': 
            if form.is_valid(): 
                add_record = form.save() 
                messages.success(request, "Record Saved") 
                return redirect('home') 
        return render(request, 'add_record.html',{'form': form}) 

    else: 
        messages.success(request, "You must be logged in") 
        return redirect('home') 
    


def update_record(request, pk): 
    if request.user.is_authenticated: 
        current_record = Records.objects.get(id=pk) 
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid(): 
            form.save()
            messages.success(request, "Record has been updated") 
            return redirect('home') 

        return render(request, 'update_record.html', {'form' : form})

    else: 
        messages.success(request, "You must be Logged In to Update the Record")
        return redirect('home') 
     
