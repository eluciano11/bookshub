from django.contrib import admin

from .models import Book


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'price', 'start_date', 'quantity')

admin.site.register(Book, BookAdmin)
