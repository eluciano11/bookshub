from django.contrib import admin

from .models import Book, Review, Category, Requested, Viewed

from reversion import VersionAdmin


class BookAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = ('title', 'edition', 'author', 'publisher')


class ReviewAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = ('user', 'book', 'review', 'pub_date')


# class ImageAdmin(VersionAdmin, admin.ModelAdmin):
#     list_display = ('book', 'image')


class RequestedAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'isbn_10', 'isbn_13')


class ViewedAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = ('user', 'book')

admin.site.register(Book, BookAdmin)
admin.site.register(Review, ReviewAdmin)
# admin.site.register(Image, ImageAdmin)
admin.site.register(Category)
admin.site.register(Requested, RequestedAdmin)
admin.site.register(Viewed, ViewedAdmin)
