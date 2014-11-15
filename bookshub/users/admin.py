from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from reversion import VersionAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import User, Review


class CustomUserAdmin(UserAdmin, VersionAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    filter_horizontal = ()
    ordering = ('email', )
    readonly_fields = ('token',)
    list_display = ('email', 'first_name', 'last_name', 'is_admin')
    list_filter = ('is_staff', 'is_superuser', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),

        (('Personal info'), {
            'fields': ('first_name', 'last_name')
        }),

        (('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),

        (('Additional data'), {
            'fields': ('title', 'facebook_url', 'twitter_url', 'gravatar_url',
                       'google_url', 'token', 'last_login')
        }),
    )
    add_fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password1', 'password2')}),
    )


class UserReviewAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = ('owner', 'score', 'text')

admin.site.register(User, CustomUserAdmin)
admin.site.register(Review, UserReviewAdmin)
admin.site.unregister(Group)
