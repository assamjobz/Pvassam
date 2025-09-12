from django.contrib import admin
from .models import User, Organization, JobPost, Application

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'is_verified')
    list_filter = ('is_verified',)
    search_fields = ('name',)
    actions = ['approve_organizations']

    def approve_organizations(self, request, queryset):
        queryset.update(is_verified=True)
    approve_organizations.short_description = "Approve selected organizations"

admin.site.register(User)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(JobPost)
admin.site.register(Application)
