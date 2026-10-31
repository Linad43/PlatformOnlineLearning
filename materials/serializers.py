from rest_framework import serializers

from .models import Course, Lesson
from .permissions import is_moderator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ('owner',)

    def validate_course(self, course):
        request = self.context.get('request')

        if (
                request
                and request.user.is_authenticated
                and not is_moderator(request.user)
                and course.owner_id != request.user.id
        ):
            raise serializers.ValidationError(
                'Нельзя привязать урок к чужому курсу.'
            )

        return course


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ('owner',)

    def get_lessons_count(self, obj):
        return obj.lessons.count()
