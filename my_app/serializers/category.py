from rest_framework import serializers

from my_app.models import Category


class CategoryNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
