from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User as AuthenticationUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import UserProfile, GitHubProfile


# Create your views here.
def home_page(request):
    return render(request, 'core/homepage.html', {})


def signin(request):
    mobile_number = request.POST['mobile']
    password = request.POST['password']
    user = authenticate(username=mobile_number, password=password)
    if user:
        login(request, user)
        user_profile = UserProfile.objects.get(mobile=mobile_number)
        return render(request, 'core/login.html', {'user_profile': user_profile})
        # return HttpResponse("Succesfully logged in {}".format(user.first_name))
    else:
        return HttpResponse("Incorrect phone number or password.")


def signup_page(request):
    return render(request, 'core/signuppage.html', {})


def signup(request):
    name = request.POST['name']
    email = request.POST['email']
    mobile = request.POST['mobile']
    password = request.POST['password']
    try:
        # In case user profile is present.
        user = UserProfile.objects.get(mobile=mobile)
        # user is present in auth user.
        if user.user:
            return HttpResponse("User {} already exists in the system. Try logging in.".format(mobile))
        # user might be a github user.
        auth_user = AuthenticationUser(username=mobile, password=password, email=email, first_name=name)
        auth_user.set_password(password)
        auth_user.save()
        user.user = auth_user
        user.save()
        return render(request, 'core/accountcreated.html', {})
    except:
        auth_user = AuthenticationUser(username=mobile, password=password, email=email, first_name=name)
        auth_user.set_password(password)
        auth_user.save()
        user = UserProfile(user=auth_user, name=name, email=email, mobile=mobile)
        user.save()
        return render(request, 'core/accountcreated.html', {})

@login_required
def logout_view(request):
    logout(request)
    return render(request, 'core/logout.html', {})


@login_required
def details_by_id(request, id):
    user_profile = UserProfile.objects.get(id=id)
    return render(request, 'core/iddetails.html', {'user_profile': user_profile})


@login_required
def user_details(request):
    users = UserProfile.objects.all()
    return render(request, 'core/userdetails.html', {'users': users})


@login_required
def set_password_view(request):
    return render(request, 'core/changepassword.html', {})


@login_required
def set_password(request):
    password = request.POST['password']
    auth_user = request.user
    auth_user.set_password(password)
    auth_user.save()
    return render(request, 'core/passwordsuccessful.html', {})


@login_required
def search_user(request):
    mobile = request.POST['mobile']
    user_profile = UserProfile.objects.get(mobile=mobile)
    return render(request, 'core/iddetails.html', {'user_profile': user_profile})

def account_profile(request):
    return render(request, 'core/mobiletocontinue.html', {'username': request.user.username})


def git_login(request):
    mobile = request.POST['mobile']
    username, email = request.user.username, request.user.email
    try:
        git_user = GitHubProfile.objects.get(email=email)
        user = UserProfile.objects.get(mobile=mobile)
        return render(request, 'core/login.html', {'user_profile': user})
    except:
        try:
            user = UserProfile.objects.get(mobile=mobile)

            if user.github_profile and user.github_profile.username != username:
                auth_user = AuthenticationUser.objects.get(username=username)
                logout(request)
                auth_user.delete()
                return HttpResponse("This mobile is already registered with a different github account.")
            else:
                git_user = GitHubProfile(username=username, email=email, user=request.user)
                git_user.save()
                user.github_profile = git_user
                user.save()
        except:
            git_user = GitHubProfile(username=request.user.username, email=request.user.email, user=request.user)
            git_user.save()
            user = UserProfile(email=email, name=username, mobile=mobile)
            user.save()

        return render(request, 'core/login.html', {'user_profile': user})

