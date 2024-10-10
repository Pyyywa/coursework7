from rest_framework import serializers
from habbits.models import Habbit
from habbits.validators import (
    NiceHabbitValidator,
    RelatedHabbitPublicValidator,
    TimeHabbitValidator,
    FrequencyHabbitValidator,
)


class HabbitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habbit
        fields = (
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
        validators = [
            NiceHabbitValidator(fields),
            RelatedHabbitPublicValidator(field="link_nice_habbit"),
            TimeHabbitValidator(field="time_to_complete"),
            FrequencyHabbitValidator(field="frequency"),
        ]
