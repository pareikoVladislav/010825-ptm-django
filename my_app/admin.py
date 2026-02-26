from django.contrib import admin

from my_app.models import Book, Author, AuthorProfile, Post


admin.site.register(Book)
admin.site.register(Author)
admin.site.register(AuthorProfile)
admin.site.register(Post)
