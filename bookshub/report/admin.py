from django.contrib import admin

from .models import ReportedUser, ReportedBook

from reversion import VersionAdmin


class ReportedBookAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = ('reason', 'book', 'seller', 'sender')


class ReportedUserAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = ('reason', 'receiver')

admin.site.register(ReportedBook, ReportedBookAdmin)
admin.site.register(ReportedUser, ReportedUserAdmin)
