from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from my_app.permissions import IsAdmin
from my_app.serializers import CategoryNestedSerializer
from my_app.models import Category


class CategoryListCreateAPIView(APIView):

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdmin()]
        return [AllowAny()]


    def get(self, request: Request, *args, **kwargs) -> Response:
        queryset = Category.objects.all()

        serializer = CategoryNestedSerializer(queryset, many=True)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = CategoryNestedSerializer(
            data=request.data
        )
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )


class CategoryRetrieveUpdateDestroyAPIView(APIView):

    def get_object(self):
        try:
            object = Category.objects.get(pk=self.kwargs['pk'])
        except Category.DoesNotExist:
            return Response(
                data={'detail': 'Category not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        return object

    def get(self, request: Request, *args, **kwargs) -> Response:
        object = self.get_object()

        serializer = CategoryNestedSerializer(object)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request: Request, *args, **kwargs) -> Response:
        object = self.get_object()

        serializer = CategoryNestedSerializer(
            instance=object,
            data=request.data
        )

        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def patch(self, request: Request, *args, **kwargs) -> Response:
        object = self.get_object()

        serializer = CategoryNestedSerializer(
            instance=object,
            data=request.data,
            partial=True
        )

        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def delete(self, request: Request, *args, **kwargs) -> Response:
        object = self.get_object()

        object.delete()

        return Response(
            data={},
            status=status.HTTP_204_NO_CONTENT
        )
