from decimal import Decimal
from typing import Any

from rest_framework import serializers

from my_app.models import Book, Author, User
from my_app.serializers.category import CategoryNestedSerializer


# def validate_title(value: str) -> str:
#     if not all(word.isalnum() for word in value.split(' ')):
#         raise serializers.ValidationError(
#             "Book title must contain only alphanumeric characters."
#         )
#
#     return value


class AuthorShortInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = [
            'id',
            'first_name',
            'last_name'
        ]


class BooksSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.0"),
        write_only=True
    )
    # category = CategoryNestedSerializer()
    # author = AuthorShortInfoSerializer()

    # category = serializers.PrimaryKeyRelatedField(
    #     read_only=True,
    #     queryset=,
    #     pk_field=
    # )
    publisher = serializers.StringRelatedField()
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        # queryset=Author.objects.all(),
    )

    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'published_date',
            'price',
            'discounted_price',
            'category',
            'genre',
            'is_bestseller',
            'author',
            'publisher'
        ]


class BookCreateSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(
    #     read_only=True
    # )
    discount_percentage = serializers.DecimalField(
        max_digits=5, # 100.00
        decimal_places=2,
        required=False,
        write_only=True,
        min_value=0,
        max_value=100
    )
    # title = serializers.CharField(
    #     max_length=125,
    #     required=True,
    #     validators=[
    #         validate_title,
    #     ]
    # )

    class Meta:
        model = Book
        fields = [
            "title",
            "description",
            "published_date",
            "category",
            "genre",
            "is_bestseller",
            "pages",
            "publisher",
            "author",
            "discount_percentage",
            "price"
        ]

    def validate_title(self, value: str) -> str:
        if not all(word.isalnum() for word in value.split(' ')):
            raise serializers.ValidationError(
                "Book title must contain only alphanumeric characters."
            )

        return value

    # orig_ptrice 100
    # discount_percentage 20 -> 0.2
    # discounted_price -> orig_ptrice * discount_percentage -> 80
    def create(self, validated_data: dict[str, Any]) -> Book:
        discount_percentage = validated_data.pop("discount_percentage", None) # 60 -> 60 / 100 -> 0.6

        if discount_percentage and validated_data.get('price'):
            discounted_price = validated_data.get('price') * (discount_percentage / 100)
            validated_data['discounted_price'] = validated_data.get('price') - discounted_price

        book = Book.objects.create(**validated_data)

        return book


class BookUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        # errors = {}

        discounted_price = attrs.get("discounted_price")
        price = attrs.get("price")

        if discounted_price and price:
            if discounted_price > price:
                raise serializers.ValidationError(
                    {
                        "discounted_price": "Discounted price MUST be less then original price"
                    }
                )

        return attrs
