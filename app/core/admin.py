from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
# Register your models here.


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Define admin page for users"""

    ordering = ["id"]
    list_display = ["username", "email"]
    fieldsets = (
        (None, {"fields": ("email", "usernaame", "password", "date_joined")}),
        (
            _("Premission"),
            (
                {
                    "fields": (
                        "is_active",
                        "is_staff",
                        "is_superuser",
                    )
                }
            ),
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    readonly_fields = ["last_login", "date_joined"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
