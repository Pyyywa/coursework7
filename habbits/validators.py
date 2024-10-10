from rest_framework.serializers import ValidationError


class NiceHabbitValidator:
    """Связанная, приятная привычки и вознаграждение."""

    def __init__(self, fields):
        self.fields = fields

    def __call__(self, value):
        # вознаграждение
        habbit_reward = value.get("reward")
        # связанная привычка
        habbit_is_linked = value.get("link_nice_habbit")
        # приятная привычка
        habbit_is_pleasant = value.get("is_pleasant")
        if habbit_is_linked and habbit_reward:
            raise ValidationError(
                "Нельзя выбрать связанную привычку и вознаграждение одновременно."
            )
        if habbit_is_pleasant and habbit_reward:
            raise ValidationError("Нельзя приятной привычке назначить вознаграждение.")
        if habbit_is_pleasant and habbit_is_linked:
            raise ValidationError(
                "У приятной привычки не может быть связанной привычки."
            )


class RelatedHabbitPublicValidator:
    """Связанная привычка + приятная"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        nice_habbit = value.get(self.field)
        if nice_habbit and not nice_habbit.is_pleasant:
            raise ValidationError(
                "Связанной привычкой может быть только приятная привычка."
            )


class TimeHabbitValidator:
    """
    Время выполнения привычки не должно быть больше 120 секунд и не должно равняться 0.
    """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        time_to_complete = value.get(self.field)
        if time_to_complete > 120 or time_to_complete <= 0:
            raise ValidationError(
                "Время выполнения не должно превышать 120 сек и не должно быть равно 0."
            )


class FrequencyHabbitValidator:
    """Нельзя выполнять привычку реже, чем 1 раз в 7 дней или вовсе не выполнять."""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_val = value.get(self.field)
        if tmp_val > 7 or tmp_val <= 0:
            raise ValidationError("Нельзя выполнять привычку реже, чем 1 раз в 7 дней.")
