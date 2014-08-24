import reversion
from reversion.models import Revision, Version

from django.contrib import admin


class BaseModelAdmin(reversion.VersionAdmin, admin.ModelAdmin):

    def get_list_display(self, request):
        return self.list_display + ('date_created', 'date_modified')

admin.site.register(Revision)
admin.site.register(Version)
