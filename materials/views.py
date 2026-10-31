from rest_framework import viewsets, generics
from rest_framework.exceptions import PermissionDenied

from .models import Course, Lesson
from .permissions import MaterialPermission, is_moderator
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [MaterialPermission]

    def get_queryset(self):
        if is_moderator(self.request.user):
            return Course.objects.all()

        return Course.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [MaterialPermission]

    def get_queryset(self):
        if is_moderator(self.request.user):
            return Lesson.objects.all()

        return Lesson.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        course = serializer.validated_data['course']

        if not is_moderator(self.request.user):
            if course.owner_id != self.request.user.id:
                raise PermissionDenied(
                    'Нельзя добавлять уроки в чужой курс.'
                )

        serializer.save(owner=self.request.user)


class LessonRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    serializer_class = LessonSerializer
    permission_classes = [MaterialPermission]

    def get_queryset(self):
        if is_moderator(self.request.user):
            return Lesson.objects.all()

        return Lesson.objects.filter(owner=self.request.user)
