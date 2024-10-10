from django import forms
from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        """Скрыть пароль в профиле"""
        super().__init__(*args, **kwargs)
        self.fields["password"].widget = forms.HiddenInput()
