from rest_framework import serializers

from desk.models import Desk


class DeskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Desk
        fields = ['id', 'User', 'title', 'created_at', 'category', 'comment', 'image', 'status']
        read_only_fields = ['status']
