from urllib.request import Request

from django.db.models import Count
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from my_app.models import User
from my_app.serializers import UserListSerializer, UserDetailSerializer


# class UserListGenericView(GenericAPIView):
#     def get(self, request: Request) -> Response:
#         qs = User.objects.all()
#
#         serializer = UserListSerializer(qs, many=True)
#
#         return Response(
#             data=serializer.data,
#             status=status.HTTP_200_OK
#         )

# class UserListCreateGenericView(GenericAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserListSerializer
#
#     def get(self, request: Request) -> Response:
#         qs = self.get_queryset()
#
#         serializer = self.get_serializer(qs, many=True)
#
#         return Response(
#             data=serializer.data,
#             status=status.HTTP_200_OK
#         )
#
#     def post(self, request: Request) -> Response:
#         serializer = self.get_serializer(data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 data=serializer.data,
#                 status=status.HTTP_201_CREATED
#             )
#         return Response(
#             data=serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )


# class UserListCreateGenericView(GenericAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserListSerializer
#
#     def get(self, request: Request) -> Response:
#         qs = self.get_queryset()
#
#         serializer = self.get_serializer(qs, many=True)
#
#         return Response(
#             data=serializer.data,
#             status=status.HTTP_200_OK
#         )
#
#     def post(self, request: Request) -> Response:
#         serializer = self.get_serializer(data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 data=serializer.data,
#                 status=status.HTTP_201_CREATED
#             )
#         return Response(
#             data=serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )


class UserListCreateGenericView(ListCreateAPIView):
    queryset = User.objects.filter(deleted=False)
    serializer_class = UserListSerializer

    def list(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.get_queryset().annotate(
            books_count=Count('published_books')
        )

        serializer = self.get_serializer(queryset, many=True)

        return Response(
            data={
                "total_objects": self.get_queryset().count(),
                "results": serializer.data
            },
            status=status.HTTP_200_OK
        )

    def create(self, request: Request, *args, **kwargs) -> Response:
        data = request.data.copy()

        if 'first_name' not in data:
            data['first_name'] = 'Unknown'

        if 'last_name' not in data:
            data['last_name'] = 'Unknown'

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserRetrieveUpdateDestroyGenericView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
