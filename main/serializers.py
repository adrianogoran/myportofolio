from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Achievement, Experience


class ExperienceSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = [
            "id", "title", "description", "category", "thumbnail",
            "started_at", "ended_at",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id", "started_at"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Experience title can't contain only HTML tags.")
        return value

    def validate_description(self, value):
        return strip_tags(value).strip()

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())


class AchievementSerializer(serializers.ModelSerializer):
    """Achievement API representation; star fields are computed and read-only."""

    category_label = serializers.CharField(source="get_category_display", read_only=True)
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Achievement
        fields = [
            "id", "title", "issuer", "description", "category", "category_label",
            "date_awarded", "is_featured", "created_at",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id", "created_at"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Achievement title can't contain only HTML tags.")
        return value

    def validate_issuer(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Issuer can't contain only HTML tags.")
        return value

    def validate_description(self, value):
        return strip_tags(value).strip()

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())
