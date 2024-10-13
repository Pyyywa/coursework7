import datetime
from config.celery import app
from habbits.models import Habbit
from habbits.services import HabbitBot


@app.task
def send_message_habbit_telegram(*args, **kwargs):
    """
    Отправка сообщений в телеграм в соответствии с запланированными привычками.
    """
    # Находим полезные привычки, запланированные пользователями, имеющими телеграм ID
    habbits = (
        Habbit.objects.select_related("creator")
        .filter(is_pleasant=False, creator__id_telegram__isnull=False)
        .all()
    )
    for values in habbits:
        time_habbit = values.time.strftime("%H:%M:%S")  # время выполнения задачи
        time_now = datetime.datetime.now().strftime("%H:%M:%S")  # текущее время
        frequency = values.frequency  # периодичность выполнения
        # отсчёт от понедельника (0)
        days_habbit_list = [x for x in range(1, 8, frequency)]
        week_day = datetime.datetime.now().weekday() + 1  # текущий день недели 1-7

        # Отправка сообщений при совпадении дня недели (0-6) и времени
        if week_day in days_habbit_list and time_habbit == time_now:
            id_telegram = str(values.creator.id_telegram)
            if values.reward is None:
                text = "Я " + str(values) + ", а затем " + str(values.link_nice_habbit)
            else:
                text = "Я " + str(values) + ", а затем " + str(values.reward)
            my_habbit_bot = HabbitBot()
            my_habbit_bot.send_message(text=text, chat_id=id_telegram)
