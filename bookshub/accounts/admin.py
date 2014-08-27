from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import Account


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Account


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Account


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
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


admin.site.register(Account, CustomUserAdmin)
