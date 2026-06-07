from rest_framework import serializers
from .models import Book, Tag


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    existing_tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=False,
        write_only=True
    )
    new_tag_names = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        write_only=True
    )

    class Meta:
        model = Book
        fields = "__all__"
        extra_kwargs = {
            'cover': {'required': False}
        }

    def create(self, validated_data):
        existing_tags = validated_data.pop("existing_tag_ids", [])
        new_tag_names = validated_data.pop("new_tag_names", [])

        book = Book.objects.create(**validated_data)
        book.tags.set(existing_tags)

        for tag_name in new_tag_names:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            book.tags.add(tag)

        return book

    def update(self, instance, validated_data):
        existing_tags = validated_data.pop("existing_tag_ids", None)
        new_tag_names = validated_data.pop("new_tag_names", [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if existing_tags is not None:
            instance.tags.set(existing_tags)
            for tag_name in new_tag_names:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                instance.tags.add(tag)

        return instance