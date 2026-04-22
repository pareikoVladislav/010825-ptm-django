from django.db.models import QuerySet
from rest_framework.decorators import api_view, action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from my_app.models import Book
from my_app.permissions import IsOwnerOrReadOnly
from my_app.serializers import BooksSerializer, BookCreateSerializer, BookUpdateSerializer


class MyPageNumberPagination(PageNumberPagination):
    page_size = 10


class MyCursorPagination(CursorPagination):
    page_size = 10
    ordering = 'id'


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    permission_classes = [IsOwnerOrReadOnly] # Все разрешения в списке будут работать через AND
    # ЕСЛИ ХОТЬ ОДИН класс-разрешение выдаст False --> False будет на весь запрос

    def get_serializer_class(self):
        if self.action in {'update', 'partial_update'}:
            return BookUpdateSerializer
        if self.action == 'create':
            return BookCreateSerializer
        return BooksSerializer

    @action(detail=False, methods=['get'], url_path='my')
    def get_my(self, request: Request, *args, **kwargs) -> Response:
        print("=" * 100)
        print(f"Пользователь, который сделал запрос: {request.user}")
        print("=" * 100)

        queryset = self.get_queryset().filter(
            publisher=request.user
        )

        serializer = self.get_serializer(queryset, many=True)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def perform_create(self, serializer):
        serializer.validated_data["owner"] = ...

        serializer.save()


class BooksListFiltersGenericView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BooksSerializer
    # pagination_class = MyPageNumberPagination
    # pagination_class = LimitOffsetPagination
    # pagination_class = MyCursorPagination

    # filters
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['genre', 'author__last_name']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'published_date']



class BooksListAPIView(APIView, PageNumberPagination):
    page_size = 5

    def get_queryset(self):
        queryset = Book.objects.all()  # SELECT * FROM books;

        authors = self.request.query_params.getlist('author')
        date_from = self.request.query_params.get('from')
        date_to = self.request.query_params.get('to')
        sort_by = self.request.query_params.get('sort_by')
        sort_order = self.request.query_params.get('order', 'asc')

        if authors:
            queryset = queryset.filter(  # SELECT * FROM books WHERE author = '%s'
                author__last_name__in=authors
            )

        if date_from:
            queryset = queryset.filter(  # SELECT * FROM books WHERE author = '%s'
                published_date__year__gte=date_from
            )

        if date_to:
            queryset = queryset.filter(  # SELECT * FROM books WHERE author = '%s'
                published_date__year__lte=date_to
            )

        if sort_by:
            if sort_order == 'desc':
                sort_by = f"-{sort_by}"

            queryset = queryset.order_by(
                sort_by
            )

        return queryset

    def get_page_size(self, request: Request):
        page_size = request.query_params.get('page_size')

        if page_size and page_size.isdigit():
            return int(page_size)
        return self.page_size

    def get(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.get_queryset()

        page_size = self.get_page_size(request)
        self.page_size = page_size
        results = self.paginate_queryset(
            queryset=queryset,
            request=request,
            view=self
        )

        serializer = BooksSerializer(results, many=True)

        return self.get_paginated_response(
            data=serializer.data,
        )


# получить список всех книг
@api_view(['GET', 'POST'])
def list_create_books(request: Request) -> Response:
    if request.method == 'GET':
        # 1. Получить объекты из БД
        queryset: QuerySet[Book] = Book.objects.all()

        # 2. Преобюразовать в простые объекты
        serializer = BooksSerializer(queryset, many=True)  # QuerySet -> [dict[]]

        # 3. Вернуть результат
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
    elif request.method == 'POST':
        try:
            serializer = BookCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except ValidationError as err:
            return Response(
                data={"error": f"Validation error: {err}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def retrieve_update_destroy_book(request: Request, pk: int) -> Response:
    try:
        obj: Book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response(
            data={"error": f"Book with ID {pk} does not exist"},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        serializer = BooksSerializer(obj)  # QuerySet -> [dict[]]

        # 3. Вернуть результат
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
    elif request.method in ['PUT', 'PATCH']:
        partial = False if request.method == 'PUT' else True

        serializer = BookUpdateSerializer(instance=obj, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
    elif request.method == 'DELETE':
        obj.delete()

        return Response(
            data={"message": f"Book with ID {pk} deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
