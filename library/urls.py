"""
URL configuration for library project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from my_app.views.authors import AuthorRetrieveUpdateDestroyGenericView, AuthorListGenericView, AuthorsViewSet
from my_app.views.books import (
    list_create_books,
    retrieve_update_destroy_book,
    BooksListAPIView,
    BooksListFiltersGenericView
)

from my_app.views.categories import (
    CategoryListCreateAPIView,
    CategoryRetrieveUpdateDestroyAPIView,
)
from my_app.views.user import UserListCreateGenericView, UserRetrieveUpdateDestroyGenericView


# router = DefaultRouter()
router = SimpleRouter()

router.register('authors', AuthorsViewSet, 'authors')


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('books/', list_create_books),
    # path('books/', BooksListAPIView.as_view()),
    path('books/', BooksListFiltersGenericView.as_view()),
    path('books/<int:pk>', retrieve_update_destroy_book),
    path('categories/', CategoryListCreateAPIView.as_view()),
    path('categories/<int:pk>', CategoryRetrieveUpdateDestroyAPIView.as_view()),
    path('users/', UserListCreateGenericView.as_view()),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyGenericView.as_view()),
    # path('authors/', AuthorListGenericView.as_view()),
    # path('authors/<str:author>/', AuthorRetrieveUpdateDestroyGenericView.as_view()),
]

urlpatterns += router.urls
