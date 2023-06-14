from django.contrib import admin

from catalog.models import *


class BookAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("author", "language", "genre")
    list_display = ("title", "author", "pub_date")


# Register your models here.

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Language)
admin.site.register(Genre)
admin.site.register(BookInstance)
