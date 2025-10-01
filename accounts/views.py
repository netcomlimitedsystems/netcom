from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required

from .forms import (
    CustomUserCreationForm,
    UserUpdateForm,
    ProfileUpdateForm,
    UserLoginForm,
    AvatarForm,
    DeleteAccountForm,
)
from .models import Profile, AccountDeletionLog


@staff_member_required
def deletion_logs(request):
    query = request.GET.get("q")
    logs = AccountDeletionLog.objects.all().order_by("-deleted_at")

    if query:
        logs = logs.filter(
            Q(user__icontains=query) |
            Q(email__icontains=query) |
            Q(reason__icontains=query)
        )

    paginator = Paginator(logs, 10)  # 10 logs per page
    page = request.GET.get("page")
    logs = paginator.get_page(page)

    return render(request, "delete_logs.html", {"logs": logs, "query": query})


@login_required
def account_settings(request):
    # Ensure profile exists
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        password_form = PasswordChangeForm(user=request.user, data=request.POST)

        if "update_profile" in request.POST and user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # messages.success(request, "Profile updated successfully!")
            return redirect("account_settings")

        elif "change_password" in request.POST and password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            # messages.success(request, "Password changed successfully!")
            return redirect("account_settings")

        else:
            messages.error(request, "Please correct the errors below.")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)
        password_form = PasswordChangeForm(user=request.user)

        for field in password_form.fields.values():
            field.widget.attrs["class"] = "form-control"

    return render(request, "account_settings.html", {
        "user_form": user_form,
        "profile_form": profile_form,
        "password_form": password_form,
    })


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create(user=user)  # Ensure profile
            # messages.success(request, "Account created successfully! Please log in.")
            return redirect("login")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            Profile.objects.get_or_create(user=user)  # Ensure profile
            # messages.success(request, f"Welcome back, {user.username}!")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    for field in form.fields.values():
        field.widget.attrs["class"] = "form-control"

    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    # messages.info(request, "You have been logged out.")
    return redirect("home")
