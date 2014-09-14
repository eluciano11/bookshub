from django.contrib import admin

from .models import Book, Review, Image, Category

from reversion import VersionAdmin


class BookAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = ('title', 'owner', 'price', 'start_date', 'quantity')


class ReviewAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = ('user', 'book', 'review', 'pub_date')


class ImageAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = ('book', 'image')

admin.site.register(Book, BookAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Category)
