from django.contrib import admin

from .models import Book, Review, Image, Category


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'price', 'start_date', 'quantity')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'review', 'pub_date')


class ImageAdmin(admin.ModelAdmin):
    list_display = ('user', 'image')

admin.site.register(Book, BookAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Category)
