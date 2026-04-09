from rest_framework import serializers

from my_app.models import User


class UserListSerializer(serializers.ModelSerializer):
    books_count = serializers.IntegerField(required=False, read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            'gender',
            'date_joined',
            'books_count',
            'deleted',
        ]


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'phone',
            'role',
            'gender',
            'is_staff',
            'is_active',
            'date_joined',
        ]
