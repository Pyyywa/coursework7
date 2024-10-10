from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User
from habbits.models import Habbit


class HabbitTestCase(APITestCase):
    """Тест модели Habbit"""

    def setUp(self) -> None:
        # Тестовый пользователь
        self.user = User.objects.create(email="testuser@test.ru")

        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)

        # Тестовая привычка
        self.habbit = Habbit.objects.create(
            creator=self.user,
            place="В парке",
            time="07:00:00",
            action="Слушать музыку",
            is_pleasant=True,
            frequency=1,
            time_to_complete=10,
            is_public=True,
        )

    def test_create_habbit(self):
        """Тест CREATE habbit"""

        data = {
            "place": "Дом",
            "time": "07:00:00",
            "action": "Пить чай",
            "is_pleasant": False,
            "frequency": 2,
            "time_to_complete": 120,
        }

        habbit_create_url = reverse("habbits:habbit_create")
        response = self.client.post(habbit_create_url, data=data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(response.json().get("action"), data.get("action"))

        self.assertTrue(
            Habbit.objects.get(pk=self.habbit.pk).action, data.get("action")
        )

        # Проверяем наличие записи в базе данных
        self.assertTrue(Habbit.objects.all().exists())

        # Тестирование ошибки ввода данных о периодичности закрепления привычек
        data = {
            "place": "Дом",
            "time": "07:00:00",
            "action": "Пить чай",
            "is_pleasant": False,
            "frequency": 8,
            "time_to_complete": 120,
        }

        habbit_create_url = reverse("habbits:habbit_create")
        response = self.client.post(habbit_create_url, data=data)

        self.assertEqual(
            response.json(),
            {
                "non_field_errors": [
                    "Нельзя выполнять привычку реже, чем 1 раз в 7 дней."
                ]
            },
        )

        # Тестирование ошибки ввода данных о продолжительности закрепления привычек
        data = {
            "place": "Дом",
            "time": "07:00:00",
            "action": "Пить чай",
            "is_pleasant": False,
            "frequency": 7,
            "time_to_complete": 140,
        }

        habbit_create_url = reverse("habbits:habbit_create")
        response = self.client.post(habbit_create_url, data=data)

        self.assertEqual(
            response.json(),
            {
                "non_field_errors": [
                    "Время выполнения не должно превышать 120 сек и не должно быть равно 0."
                ]
            },
        )

    def test_list_habbit(self):
        """Тест READ LIST habbit"""

        habbit_list_url = reverse("habbits:habbit_list")

        response = self.client.get(habbit_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            Habbit.objects.get(pk=self.habbit.pk).action,
            response.json().get("results")[0].get("action"),
        )

    def test_retrieve_habbit(self):
        """Тест READ ONE habbit"""

        habbit_one_url = reverse("habbits:habbit_get", args=[self.habbit.pk])

        response = self.client.get(habbit_one_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        response = response.json()

        self.assertEqual(response.get("creator"), self.user.pk)
        self.assertEqual(response.get("place"), "В парке")
        self.assertEqual(response.get("time"), "07:00:00")
        self.assertEqual(response.get("action"), "Слушать музыку")

    def test_update_habbit(self):
        """Тест UPDATE habbit"""

        data = {
            "place": "updated place",
            "action": "updated action",
            "frequency": 3,
            "time_to_complete": 110,
        }

        habbit_update_url = reverse("habbits:habbit_update", args=[self.habbit.pk])

        response = self.client.patch(habbit_update_url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        response = response.json()

        self.assertEqual(response.get("place"), "updated place")
        self.assertEqual(response.get("action"), "updated action")
        self.assertEqual(response.get("frequency"), 3)
        self.assertEqual(response.get("time_to_complete"), 110)

    def test_delete_habbit(self):
        """Тест DELETE habbit"""

        habbit_delete_url = reverse("habbits:habbit_delete", args=[self.habbit.pk])

        response = self.client.delete(habbit_delete_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(
            Habbit.objects.all().exists(),
        )
