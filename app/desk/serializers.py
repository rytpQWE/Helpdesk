from collections import OrderedDict

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
        """
        Method override for save multiply images
        """
        uploaded_images = validated_data.pop("uploaded_images")
        desk = Desk.objects.create(**validated_data)
        if uploaded_images:
            for image in uploaded_images:
                newdesk_image = DeskImage.objects.create(desk=desk, images=image)
        return desk


class DeskCompleteSerializer(serializers.ModelSerializer):
    images_set = ImagesSerializer(many=True, source='img', read_only=True)

    class Meta:
        model = Desk
        fields = ['id', 'User', 'title', 'created_at', 'category', 'comment', 'status', 'employee_comment',
                  'images_set']

    # To delete null and '' fields
    def to_representation(self, instance):
        result = super(DeskCompleteSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] not in [None, ""]])


class EmployeeDeskSerializer(serializers.ModelSerializer):
    images_set = ImagesSerializer(many=True, source='img', read_only=True)

    class Meta:
        model = Desk
        fields = ['id', 'User', 'title', 'created_at', 'category', 'comment', 'status', 'images_set', 'employee_comment']
        read_only_fields = ['id', 'User', 'title', 'created_at', 'category', 'comment', 'images_set']
        extra_kwargs = {'employee_comment': {"required": False, "allow_null": True}}

    # To delete null fields
    def to_representation(self, instance):
        result = super(EmployeeDeskSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])
