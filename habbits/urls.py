from django.urls import path
from habbits.apps import HabbitsConfig
from habbits.views import (
    HabbitSerializeListAPIView,
    HabbitSerializeRetrieveAPIView,
    HabbitSerializeCreateAPIView,
    HabbitSerializeUpdateAPIView,
    HabbitSerializeDestroyAPIView,
)

app_name = HabbitsConfig.name
urlpatterns = [
    path("habbits/", HabbitSerializeListAPIView.as_view(), name="habbit_list"),
    path(
        "habbits/<int:pk>/", HabbitSerializeRetrieveAPIView.as_view(), name="habbit_get"
    ),
    path(
        "habbits/create/", HabbitSerializeCreateAPIView.as_view(), name="habbit_create"
    ),
    path(
        "habbits/update/<int:pk>/",
        HabbitSerializeUpdateAPIView.as_view(),
        name="habbit_update",
    ),
    path(
        "habbit/delete/<int:pk>/",
        HabbitSerializeDestroyAPIView.as_view(),
        name="habbit_delete",
    ),
]
