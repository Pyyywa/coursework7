from django.contrib import admin
from habbits.models import Habbit


@admin.register(Habbit)
class HabbitAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "creator",
        "link_nice_habbit",
        "place",
        "time",
        "action",
        "is_pleasant",
        "frequency",
        "reward",
        "time_to_complete",
        "is_public",
    )
    list_filter = (
        "creator",
        "action",
        "is_pleasant",
        "is_public",
    )
    search_fields = (
        "action",
        "is_pleasant",
        "reward",
        "place",
    )
