from rest_framework.serializers import ModelSerializer, SerializerMethodField
from materials.models import Course, Lesson, Subscription
from materials.validators import VideoValidators


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [VideoValidators(field="video_url")]


class CourseSerializer(ModelSerializer):
    lesson_count = SerializerMethodField()
    lesson = LessonSerializer(source="lessons", many=True, read_only=True)
    subscription = SerializerMethodField()

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    def get_subscription(self, obj):
        subscription = Subscription.objects.filter(
            course=obj,
            owner=self.context.get("request").user
        ).all()
        if subscription:
            return True
        else:
            return False

    class Meta:
        model = Course
        fields = ("id", "title", "preview", "description", "lesson_count", "lesson")


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = ("id", "owner", "course")
