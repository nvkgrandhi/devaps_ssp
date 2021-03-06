import logging
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User

from .forms import LoginForm, RegistrationForm
from .models import UserProfile
# Create your views here.

logger = logging.getLogger(__name__)


def home(request):
    logger.info('Calling Home Page Function')
    return render(request, 'index.html')


def admin_home(request):
    logger.info('Calling Admin Page Function')
    return render(request, 'admin.html', {'user': 'admin'})


def login_page(request):
    logger.info('Calling Login Page Function')
    return render(request, 'login.html')


def login(request):
    logger.info('Calling login Function')
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
                    error = 'Please enter username and password to login'
                    return render(request, 'login.html', {'error': error, 'form': form})
            except:
                error = 'Invalid User Please Enter Valid User Name and Password'
                return render(request, 'login.html', {'error': error, 'form': form})
        else:
            error = 'Please enter username and password to login'
            return render(request, 'login.html', {'error': error})

    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


def logout(request):
    logger.info('Calling Logout Function')
    return render(request, 'login.html')


def create_user(request):
    logger.info('Calling Create User Function')
    return render(request, 'create_user.html',)


def register(request):
    logger.info('Calling Register User Function')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                auth_user = User()
                auth_user.first_name = request.POST.get('first_name')
                auth_user.last_name = request.POST.get('last_name')
                auth_user.username = request.POST.get('username')
                auth_user.password = request.POST.get('password')
                auth_user.email = request.POST.get('email')
                auth_user.is_superuser = False
                auth_user.is_staff = True
                auth_user.save()
                auth_user_profile = UserProfile()
                auth_user_profile.role = request.POST.get('role')
                auth_user_profile.user_id = auth_user.id
                auth_user_profile.save()
            except:
                error = 'Invalid Data'
                return render(request, 'create_user.html', {'error': error})
        else:
            error = 'Pleae Fill the below details! All are mandatory'
            return render(request, 'create_user.html', {'error': error})
    else:
        form = RegistrationForm()
        return render(request, 'create_user.html', {'form': form})

    return render(request, 'register_success.html')


def list_users(request):
    logger.info('Calling List All User Function')
    auth_user = User.objects.all()
    data = {'object_list': auth_user}
    return render(request, 'list_users.html', data)


def update(request):
    logger.info('Calling Edit User Function')
    auth_user = UserProfile.objects.all()
    data = {'object_list': auth_user}
    return render(request, 'update_user.html', data)


def update_user(request, user_id):
    logger.info('Calling Edit User Function')
    if request.method == 'POST':
        auth_user = UserProfile.objects.get(user_id=user_id)
        auth_user.role = request.POST.get('role')
        auth_user.save()

    auth_user = UserProfile.objects.all()
    data = {'object_list': auth_user}
    return render(request, 'update_user.html', data)


def delete(request):
    pass


def delete_user(request, user_id):
    logger.info('Calling Delete User Function')
    auth_user = User.objects.get(pk=user_id)
    auth_user.delete()
    auth_user = User.objects.all()
    data = {'object_list': auth_user}
    return render(request, 'list_users.html', data)


def user_view(request):
    logger.info('Calling User View Function')
    return render(request, 'user.html')
