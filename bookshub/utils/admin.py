import reversion
from reversion.models import Revision, Version

from django.contrib import admin


class BaseModelAdmin(reversion.VersionAdmin, admin.ModelAdmin):

    def get_list_display(self, request):
        return self.list_display + ('created_at', 'modified_at')

admin.site.register(Revision)
admin.site.register(Version)
