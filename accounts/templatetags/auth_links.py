from django import template
from django.urls import reverse
from django.utils.html import format_html

register = template.Library()

@register.simple_tag(takes_context=True)
def auth_link(context, viewname, icon, label):
    """
    Renders a sidebar link. If user is not authenticated,
    clicking will open the auth modal instead.
    """
    user = context['request'].user

    if user.is_authenticated:
        url = reverse(viewname)
        return format_html(
            '<a class="nav-link d-flex align-items-center" href="{}">'
            '<i class="bi {} me-2"></i>{}</a>',
            url, icon, label
        )
    else:
        return format_html(
            '<a class="nav-link d-flex align-items-center" href="#" '
            'data-bs-toggle="modal" data-bs-target="#authModal">'
            '<i class="bi {} me-2"></i>{}</a>',
            icon, label
        )

@register.simple_tag(takes_context=True)
def auth_logout(context):
    """
    Shows Logout if logged in, otherwise shows Login/Register (modal).
    """
    user = context['request'].user

    if user.is_authenticated:
        url = reverse("logout")
        return format_html(
            '<a class="nav-link d-flex align-items-center text-danger" href="{}">'
            '<i class="bi bi-box-arrow-right me-2"></i>Logout</a>', url
        )
    else:
        return format_html(
            '<a class="nav-link d-flex align-items-center text-info" href="#" '
            'data-bs-toggle="modal" data-bs-target="#authModal">'
            '<i class="bi bi-box-arrow-in-right me-2"></i>Login / Register</a>'
        )
