from django.contrib import admin
from django import forms

from .models import Offer, Image

from reversion import VersionAdmin
from django_filepicker.widgets import FPFileWidget


class MyImageFormAdmin(forms.ModelForm):
    class Meta:
        model = Image
        widgets = {
            'image': FPFileWidget
        }


class OfferAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = (
        'book', 'owner', 'price', 'quantity', 'start_date',)


class ImageAdmin(VersionAdmin, admin.ModelAdmin):
    form = MyImageFormAdmin
    list_display = ('offer', 'image',)

admin.site.register(Offer, OfferAdmin)
admin.site.register(Image, ImageAdmin)
