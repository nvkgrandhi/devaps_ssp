import logging
import os
import select
import sys
import time

import paramiko
import requests
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

from .forms import LoginForm, RegistrationForm
from .models import UserProfile
from devaps_ssp.settings import BASE_DIR

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


def create_file(request):
    logger.info('Function to create script')
    if request.method == 'POST':
        file = open(os.path.join(BASE_DIR, 'scripts/script.py'), 'w')
        return HttpResponse('File has been created successfully')
    else:
        return HttpResponse('Something went wrong! not able to create file')


def execute_jenkins(request):
    logger.info('Function to execute script')
    if request.method == 'POST':
        vcs = request.POST.get('vcs')
        crt = request.POST.get('cr')
        buildt = request.POST.get('bd')
        host = '10.76.205.223'
        i = 1

        if vcs == 'Git' and crt == 'Gerrit' and buildt == 'Jenkins':
            print('Porperly Selected the Tools')
            message = "Selected Tools are {} | {} | {}. Selected Tools are ready to Run".format(vcs, crt, buildt)
            if message is not None:
                messages.info(request, message)
            else:
                messages.error(request, 'Error')

            while True:
                print('Trying to connect to %s (%i/10)' %(host, i))
                message_i = "Trying to connect to %s (%i/10)" %(host, i)
                if message_i is not None:
                    messages.info(request, message_i)
                else:
                    messages.error(request, 'Error')

                try:
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(host, username='root', password='123456')
                    message_ii = 'Connected to %s' %host
                    if message_ii is not None:
                        messages.info(request, message_ii)
                    else:
                        messages.error(request, 'Error')

                    print('Connected to %s' % host)
                    break
                except paramiko.AuthenticationException:
                    message_ii = "Authentication failed when connecting to %s" % host
                    if message_ii is not None:
                        messages.info(request, message_ii)
                    else:
                        messages.error(request, 'Error')
                    print("Authentication failed when connecting to %s" % host)
                    sys.exit(1)
                except:
                    message_ii = "Could not SSH to %s, waiting for it to start" % host
                    if message_ii is not None:
                        messages.info(request, message_ii)
                    else:
                        messages.error(request, 'Error')
                    print("Could not SSH to %s, waiting for it to start" % host)
                    i += 1
                    time.sleep(2)

                # If we could not connect within time limit
                if i == 10:
                    message_i = "Could not connect to %s. Giving up" % host
                    if message_i is not None:
                        messages.info(request, message_i)
                    else:
                        messages.error(request, 'Error')
                    print("Could not connect to %s. Giving up" % host)
                    sys.exit(1)

            # Send the command (non-blocking)
            stdin, stdout, stderr = ssh.exec_command("java -jar /home/victor/jenkins-cli.jar -s http://10.76.205.223:8080/ build 'warproj1' -s")
            # stdin, stdout, stderr = ssh.exec_command("java -jar /home/victor/jenkins-cli.jar -s http://10.76.205.223:8080/ build 'warproj1' -s")

            # Wait for the command to terminate
            while not stdout.channel.exit_status_ready():
                # Only print data if there is data to read in the channel
                if stdout.channel.recv_ready():
                    rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
                    if len(rl) > 0:
                        # Print data from stdout
                        data = stdout.channel.recv(1024)
                        if data is not None:
                            messages.info(request, data)
                        else:
                            messages.error(request, 'Error')
                        print(stdout.channel.recv(1024)),

            # Disconnect from the host
            message_vi = "Command has been executed on Jenkins Build Server"
            if message_vi is not None:
                messages.info(request, message_vi)
            else:
                messages.error(request, 'Error')
            print("Command has been executed on Jenkins Build Server")
            ssh.close()
        else:
            print("Please select Proper Tools")
            message = '....Oops select tools are not configurable {} | {} | {}  - - - ' \
                      'Please select Git | Gerrit | Jenkins Only'.format(vcs, crt, buildt)
            if message is not None:
                messages.info(request, message)
            else:
                messages.error(request, 'Error')
            # sys.exit(1)

    return render(request, 'results.html')


def auth_git(request):
    logger.info("Calling auth_git function to authenticate github account")
    import pdb; pdb.set_trace();

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        r = requests.get('https://api.github.com', auth=(username, password))

        print(r.status_code)
        print(r.headers['content-type'])

    return HttpResponse(r.status_code)





