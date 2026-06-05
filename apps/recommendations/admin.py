from django.contrib import admin

from .models import (
    Book,
    Tag
)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "author",
        "status",
        "uploaded_by",
        "created_at"
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "title",
        "author"
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):

    search_fields = (
        "name",
    )