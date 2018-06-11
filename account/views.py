from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.core.files.base import ContentFile
from urllib import request as request_lib

from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile
from .utils import check_mail_validity_with_email_hippo, check_mail_validity_with_email_hunter, get_person_detail_based_on_provided_email, check_mail_validity_with_never_bounce, code_generator


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
            response = check_mail_validity_with_never_bounce(mail)
            print(response)
            if response != 'disposable' and response != 'valid':
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
            new_user.is_active = False
            new_user.save()
            profile = new_user.profile
            try:
                photo_url = user_data['avatar']
                response = request_lib.urlopen(photo_url)
                image_name = '{}.jpg'.format(slugify(new_user.username))
                profile.photo.save(image_name, ContentFile(response.read()))
                profile.save()
            except (TypeError, AttributeError):
                pass
            profile.activation_key = code_generator()
            path = reverse('account:activate', kwargs={"code": profile.activation_key})
            full_path = settings.SITE_URL + path
            subject = 'Activate Account'
            from_email = settings.DEFAULT_FROM_EMAIL
            message = f'Activate your account here: {full_path}'
            recipient_list = [new_user.email]
            html_message = f'<p>Activate your account here: {full_path}</p>'
            send_mail(subject, message, from_email, recipient_list, fail_silently=False, html_message=html_message)
            profile.save()
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


def activate_user_view(request, code=None, *args, **kwargs):
    if code:
        qs = Profile.objects.filter(activation_key=code)
        if qs.exists() and qs.count() == 1:
            profile = qs.first()
            user = profile.user
            if not user.is_active:
                user.is_active = True
                user.save()
                return render(request, 'account/account_activated.html', {"user": user})
    return redirect(reverse('account:login'))
