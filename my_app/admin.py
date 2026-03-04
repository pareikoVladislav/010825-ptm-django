from django.contrib import admin

from my_app.models import Book, Author, AuthorProfile, Post


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "price",
        "category",
        "published_date"
    ]

    search_fields = [
        "title",
    ]

    list_filter = [
        "published_date",
        "category"
    ]

    list_editable = [
        "category",
        "price"
    ]

    list_per_page = 25


# admin.site.register(Book, BookAdmin)

admin.site.register(Author)
admin.site.register(AuthorProfile)
admin.site.register(Post)
