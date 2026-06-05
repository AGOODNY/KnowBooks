from rest_framework import serializers
from .models import Book, Tag


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):

    tags = TagSerializer(
        many=True,
        read_only=True
    )

    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        write_only=True,
        required=False
    )

    class Meta:
        model = Book
        fields = "__all__"

    def create(self, validated_data):

        tags = validated_data.pop(
            'tag_ids',
            []
        )

        book = Book.objects.create(
            **validated_data
        )

        book.tags.set(tags)

        return book

    def update(self, instance, validated_data):

        tags = validated_data.pop(
            'tag_ids',
            None
        )

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if tags is not None:
            instance.tags.set(tags)

        return instance