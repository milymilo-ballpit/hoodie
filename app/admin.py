from django.contrib import admin
from django.contrib.postgres import fields
from django.db.models import Count
from django.urls import reverse
from django.utils.safestring import mark_safe

from django_json_widget.widgets import JSONEditorWidget
from .models import Link, Entry


class EntryInline(admin.StackedInline):
    formfield_overrides = {
        fields.JSONField: {'widget': JSONEditorWidget},
    }

    model = Entry
    extra = 0


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "entries",
        "inbound",
        "outbound",
    )

    search_fields = ("__all__",)

    inlines = [EntryInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(_entry_count=Count("entries"))
        return queryset

    def entries(self, obj):
        return obj._entry_count

    entries.admin_order_field = '_entry_count'


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    formfield_overrides = {
        fields.JSONField: {'widget': JSONEditorWidget},
    }

    list_display = (
        "id",
        "link_link",
        "has_browser_data",
        "correlation_id",
    )

    search_fields = ("link__name", "correlation_id")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related("link")
        return queryset

    def link_link(self, obj):
        return mark_safe(
            '<a href="{}">{}</a>'.format(
                reverse("admin:app_link_change",
                        args=(obj.link.pk,),),
                obj.link.name,
            )
        )

    link_link.short_description = "link instance"
