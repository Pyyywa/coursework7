from django.db.models import Q
from rest_framework import generics

from habbits.models import Habbit
from habbits.paginators import HabbitPaginator
from habbits.permissions import IsCreator
from habbits.serializers import HabbitSerializer
from rest_framework.permissions import IsAuthenticated


class HabbitSerializeListAPIView(generics.ListAPIView):
    serializer_class = HabbitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HabbitPaginator

    def get_queryset(self):
        """Фильтрация запроса:
        привычки текущего пользователя или публичные"""
        user = self.request.user
        return Habbit.objects.filter(Q(creator=user) | Q(is_public=True))


class HabbitSerializeRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = HabbitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Фильтрация запроса:
        привычки текущего пользователя или публичные"""
        user = self.request.user
        return Habbit.objects.filter(Q(creator=user) | Q(is_public=True))


class HabbitSerializeCreateAPIView(generics.CreateAPIView):
    serializer_class = HabbitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Привязка пользователя к создаваемой привычке"""
        new_habbit = serializer.save()
        new_habbit.creator = self.request.user
        new_habbit.save()


class HabbitSerializeUpdateAPIView(generics.UpdateAPIView):
    serializer_class = HabbitSerializer
    queryset = Habbit.objects.all()
    permission_classes = [IsAuthenticated, IsCreator]


class HabbitSerializeDestroyAPIView(generics.DestroyAPIView):
    queryset = Habbit.objects.all()
    permission_classes = [IsAuthenticated, IsCreator]
