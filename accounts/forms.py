from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile


# 🔹 User Registration
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your email"
        })
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["autocomplete"] = "off"


# 🔹 Update User Info (username + email)
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["autocomplete"] = "off"


# 🔹 Update Profile (avatar + bio)
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar", "bio"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["avatar"].widget.attrs.update({"class": "form-control"})
        if "bio" in self.fields:
            self.fields["bio"].widget.attrs.update({
                "class": "form-control",
                "rows": 3,
                "placeholder": "Tell us about yourself..."
            })


# 🔹 Avatar-only form (if separate upload is needed)
class AvatarForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar"]


# 🔹 Login Form
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )


# 🔹 Delete Account Form (confirm + optional reason)
class DeleteAccountForm(forms.Form):
    confirm = forms.BooleanField(required=True, label="Yes, I want to delete my account.")
    reason = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"placeholder": "Optional: Why are you leaving?", "rows": 3}),
        label="Reason for deleting account"
    )
