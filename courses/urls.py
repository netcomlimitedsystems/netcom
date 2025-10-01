from django.urls import path
from . import views
from accounts import views as account_views

urlpatterns = [
    path("", views.home, name="home"),
    
    path("courses/", views.courses_view, name="courses"),
    path("blog/", views.blog, name="blog"),
    path("cybersecurity/", views.cybersecurity, name="cybersecurity"),
    path("cloud/",views.cloud_view, name="cloud"),
    
    path("software/", views.software, name="software"),
    path("profile/", views.profile, name="profile"),
    path("account/settings/", views.account_settings, name="account_settings"),
    
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),

    # Auth
    path("register/", account_views.register_view, name="register"),
    path("login/", account_views.login_view, name="login"),
    path("logout/", account_views.logout_view, name="logout"),
]
