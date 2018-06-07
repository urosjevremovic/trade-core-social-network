from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.files.base import ContentFile
from urllib import request as request_lib

from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile
from .utils import check_mail_validity_with_email_hippo, check_mail_validity_with_email_hunter, get_person_detail_based_on_provided_email


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            mail = user_form.cleaned_data['email']
            response = check_mail_validity_with_email_hippo(mail)
            if response != 'Ok':
                messages.error(request, "Please enter a valid email address")
                return redirect('account:register')
            user_data = get_person_detail_based_on_provided_email(mail)
            try:
                new_user.first_name = user_data['name']['givenName']
                new_user.last_name = user_data['name']['familyName']
            except TypeError:
                pass
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.username = new_user.username.capitalize()
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            try:
                photo_url = user_data['avatar']
                response = request_lib.urlopen(photo_url)
                image_name = '{}.jpg'.format(slugify(new_user.username))
                profile.photo.save(image_name, ContentFile(response.read()))
                profile.save()
            except TypeError:
                pass
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully")
            return redirect('dashboard')
        else:
            messages.error(request, "Error occurred while updating your profile")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def user_list(request):
    users = User.objects.all().exclude(username=request.user.username)
    return render(request, 'account/list.html', {'section': 'people', 'users': users})


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'account/detail.html', {'section': 'people', 'user': user})
