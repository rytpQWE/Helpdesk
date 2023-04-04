from rest_framework import serializers

from desk.models import Desk, DeskImage


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeskImage
        fields = ['images']


class DeskCreateSerializer(serializers.ModelSerializer):
    images_set = ImagesSerializer(many=True, source='img', read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=100000, allow_empty_file=True, use_url=False),
        write_only=True,
        default=None,
        required=False,
    )

    class Meta:
        model = Desk
        fields = ['id', 'User', 'title', 'created_at', 'category', 'comment', 'status', 'images_set', 'uploaded_images']
        read_only_fields = ['status', 'User']
        extra_kwargs = {'uploaded_images': {"required": False, "allow_null": True}}

    # Upload files(images) only in postman
    def create(self, validated_data):
        """Method override for save multiply images"""
        uploaded_images = validated_data.pop("uploaded_images")
        desk = Desk.objects.create(**validated_data)
        if uploaded_images is None:
            pass
        else:
            for image in uploaded_images:
                newdesk_image = DeskImage.objects.create(desk=desk, images=image)
        return desk


class AdminDeskSerializer(serializers.ModelSerializer):
    images_set = ImagesSerializer(many=True, source='img', read_only=True)

    class Meta:
        model = Desk
        fields = ['id', 'User', 'title', 'created_at', 'category', 'comment', 'status', 'images_set']
        read_only_fields = ['id', 'User', 'title', 'created_at', 'category', 'comment', 'images_set']
