from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from .models import UserGroup

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin panel configuration for Custom User model.
    """
    # Fields to display in admin list view
    list_display = ("username", "email", "first_name", "last_name", "is_staff")

    # Fields editable in list view (optional)
    list_editable = ("email",)

    # Add followed_organizations as filter or in fieldsets
    filter_horizontal = ("groups", "user_permissions", "followed_organizations")

    # Fieldsets control how fields are grouped in user edit page
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        ("Permissions", {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")
        }),
        ("Followed Organizations", {"fields": ("followed_organizations",)}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    # Fields used when creating a new user via admin
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2"),
        }),
    )


admin.site.unregister(Group)


@admin.register(UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    pass
