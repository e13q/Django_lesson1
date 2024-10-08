from django.contrib import admin
from places.models import Image, Place
from django.utils.html import format_html
from adminsortable2.admin import SortableAdminBase, SortableInlineAdminMixin

class ImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Image
    extra = 0
    readonly_fields = ["image_preview", ]
    fields = ['image', 'image_preview',]

    def image_preview(self, obj):
        return format_html('<img src="{url}" width="255px" height="200px" />'.format(
            url = obj.image.url
            )
        )

@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [ImageInline,] 