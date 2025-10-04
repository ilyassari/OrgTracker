from django.contrib import admin
from .models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'org_type', 'nation', 'founding_date', 'headcount')
    list_filter = ('org_type', 'nation', 'founding_date')
    search_fields = ("name", "slug")
    ordering = ("name",)
    readonly_fields = ("slug",)
