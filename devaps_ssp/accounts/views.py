from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User

from .forms import LoginForm, RegistrationForm
from .models import UserProfile
# Create your views here.


def home(request):
    return render(request, 'index.html')


def login_page(request):
    return render(request, 'login.html')


def login(request):
    # import pdb; pdb.set_trace()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                username = request.POST.get('username')
                password = request.POST.get('password')
                auth_user = User.objects.get(username=username)
                auth_user.password = password
                if auth_user is not None:
                    if auth_user.username == 'admin' and auth_user.password == password :
                        if auth_user.is_active:
                            return render(request, 'admin.html', {'user': auth_user.username})
                        else:
                            error = 'Invalid User'
                            return render(request, 'admin.html', {'error': error})
                    else:
                        if auth_user.is_active:
                            return render(request, 'user.html', {'user': auth_user.username})
                        else:
                            error = 'Invalid User'
                            return render(request, 'user.html', {'error': error})
                else:
                    error = 'Please enter valid username and password to login'
                    return render(request, 'login.html', {'error': error, 'form': form})
            except:
                error = 'Invalid User Please Enter Valid User Name and Password'
                return render(request, 'login.html', {'error': error, 'form': form})
        else:
            error = 'Please enter valid username and password to login'
            return render(request, 'login.html', {'error': error})

    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


def logout(request):
    return render(request, 'login.html')


def create_user(request):
    return render(request, 'create_user.html',)


def register(request):
    import pdb; pdb.set_trace();
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            return HttpResponse('form is valid')
        else:
            error = 'Pleae Fill the below details! All are mandatory'
            return render(request, 'create_user.html', {'error': error})
    else:
        return HttpResponse('invalid request')


def list_users(request):
    pass


def update_user(request):
    pass


def delete_user(request, user_id):
    pass


def user_view(request):
    pass

