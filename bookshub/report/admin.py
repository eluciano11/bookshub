from django.contrib import admin

from .models import ReportedUser, ReportedBook, ReportedOffer

from reversion import VersionAdmin


class ReportedBookAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = ('reason', 'book', 'seller', 'sender')


class ReportedUserAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = ('reason', 'receiver')


class ReportedOfferAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = ('reason', 'sender', 'offer')

admin.site.register(ReportedBook, ReportedBookAdmin)
admin.site.register(ReportedUser, ReportedUserAdmin)
admin.site.register(ReportedOffer, ReportedOfferAdmin)
