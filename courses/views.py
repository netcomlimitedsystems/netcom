from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import models
from .models import Course
from django.core.paginator import Paginator
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Course, Lesson, Enrollment, Blog

@staff_member_required
def admin_dashboard(request):
    stats = {
        "users": User.objects.count(),
        "courses": Course.objects.count(),
        "lessons": Lesson.objects.count(),
        "enrollments": Enrollment.objects.count(),
        "blogs": Blog.objects.count(),
    }

    recent_courses = Course.objects.order_by("-created_at")[:5]
    recent_enrollments = Enrollment.objects.select_related("user", "course").order_by("-enrolled_at")[:5]
    recent_blogs = Blog.objects.order_by("-published_at")[:5]

    # For charts
    course_popularity = Course.objects.annotate(enroll_count=models.Count("enrollments")).order_by("-enroll_count")[:5]

    context = {
        "stats": stats,
        "recent_courses": recent_courses,
        "recent_enrollments": recent_enrollments,
        "recent_blogs": recent_blogs,
        "course_popularity": course_popularity,
    }
    return render(request, "admin/admin_dashboard.html", context)

def courses_view(request):
    courses = None
    page_obj = None

    if request.user.is_authenticated:
        # ✅ Authenticated users can see real courses
        course_list = Course.objects.all().order_by("title")

        # Pagination setup (10 per page, adjust if needed)
        paginator = Paginator(course_list, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        # Get the courses for the current page
        courses = page_obj.object_list

    # ✅ Guests will NOT be redirected
    # They’ll just see guest_content from base.html
    return render(request, "courses.html", {
        "courses": courses,
        "page_obj": page_obj,
    })


def home(request):
    return render(request, "home.html")


@login_required(login_url="login")
def blog(request):
    return render(request, "blog.html")


# @login_required(login_url="login")
def cybersecurity(request):
    courses = None

    if request.user.is_authenticated:
        # Only Cybersecurity courses for logged-in users
        courses = Course.objects.filter(category="cybersecurity").order_by("title")


    # Guests won’t be redirected → they will see guest_content in the template
    return render(request, "cybersecurity.html", {
        "courses": courses,
    })


def software(request):
    courses = None
    if request.user.is_authenticated:
        courses = Course.objects.filter(category="software").order_by("title")
    return render(request, "software.html", {"courses": courses})


def cloud_view(request):
    courses = None
    if request.user.is_authenticated:
        courses = Course.objects.filter(level="beginner").order_by("title")
    return render(request, "cloud.html", {"courses": courses})


def devops_view(request):
    courses = None
    if request.user.is_authenticated:
        courses = Course.objects.filter(category="devops").order_by("title")
    return render(request, "devops.html", {"courses": courses})





@login_required(login_url="login")
def profile(request):
    return render(request, "profile.html")


@login_required(login_url="login")
def account_settings(request):
    return render(request, "account_settings.html")
