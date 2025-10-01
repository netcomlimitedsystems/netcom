from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("settings/", views.account_settings, name="account_settings"),
    path("deletion-logs/", views.deletion_logs, name="deletion_logs"),  # already added
]
