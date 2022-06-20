from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render


from authentication.forms import LoginForm, UserRegisterForm


def user_login(request):
    context = {'login_form': LoginForm()}
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username = username, password= password)
            if user:
                login(request,user)
                return redirect('list_items')
    return render(request, 'auth/login.html', context)


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # щоб зразу зайти після реєстрацї
            messages.success(request, 'Registation success !')
            return redirect('list_items')
        else:
            messages.error(request, 'Error of registration')
    else:
        form = UserRegisterForm()
    return render(request, 'auth/register.html', {'form':form})


def user_logout(request):
    logout(request)
    # return redirect('auth/login.html')
    return redirect('list_items')

