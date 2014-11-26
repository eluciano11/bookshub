from django.contrib import admin
from django import forms

from .models import Book, Review, Category, Requested, Viewed

from reversion import VersionAdmin

from django_filepicker.widgets import FPFileWidget


class MyBookFormAdmin(forms.ModelForm):
    class Meta:
        model = Book
        widgets = {
            'image': FPFileWidget
        }


class BookAdmin(VersionAdmin, admin.ModelAdmin):
    form = MyBookFormAdmin
    list_display = ('title', 'edition', 'author', 'publisher')


class ReviewAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = ('user', 'book', 'review')


class RequestedAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'isbn_10', 'isbn_13')


class ViewedAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = ('user', 'book')

admin.site.register(Book, BookAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Category)
admin.site.register(Requested, RequestedAdmin)
admin.site.register(Viewed, ViewedAdmin)
