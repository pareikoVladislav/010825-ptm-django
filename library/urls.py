from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)

from my_app.views.authors import (
    AuthorRetrieveUpdateDestroyGenericView,
    AuthorListGenericView,
    AuthorsViewSet
)
from my_app.views.books import (
    list_create_books,
    retrieve_update_destroy_book,
    BooksListAPIView,
    BooksListFiltersGenericView,
    BookViewSet
)

from my_app.views.categories import (
    CategoryListCreateAPIView,
    CategoryRetrieveUpdateDestroyAPIView,
)
from my_app.views.user import (
    UserListCreateGenericView,
    UserRetrieveUpdateDestroyGenericView, LoginUser, LogoutUser
)


# router = DefaultRouter()
router = SimpleRouter()

router.register('authors', AuthorsViewSet, 'authors')
router.register('books', BookViewSet, 'books')


urlpatterns = [
    path('admin/', admin.site.urls),

    path('auth-token/', obtain_auth_token),
    # JWT
    path('jwt-login/', TokenObtainPairView.as_view()),
    path('refresh-token/', TokenRefreshView.as_view()),
    path('api-auth/', include('rest_framework.urls')),

    # custom auth
    path('auth-login/', LoginUser.as_view()),
    path('auth-logout/', LogoutUser.as_view()),

    path('categories/', CategoryListCreateAPIView.as_view()),
    path('categories/<int:pk>', CategoryRetrieveUpdateDestroyAPIView.as_view()),
    path('users/', UserListCreateGenericView.as_view()),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyGenericView.as_view()),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # path('books/', list_create_books),
    # path('books/', BooksListAPIView.as_view()),
    # path('books/', BooksListFiltersGenericView.as_view()),
    # path('books/<int:pk>', retrieve_update_destroy_book),
    # path('authors/', AuthorListGenericView.as_view()),
    # path('authors/<str:author>/', AuthorRetrieveUpdateDestroyGenericView.as_view()),
]

urlpatterns += router.urls
