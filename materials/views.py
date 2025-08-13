from rest_framework.viewsets import ModelViewSet
from materials.models import Course, Lesson, Subscription
from materials.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from users.permissions import IsModerator, IsOwner
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from materials.paginations import CoursePagination, LessonPagination
from materials.tasks import send_email_for_update_course


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePagination

    def perform_create(self, serializer):
        """Привязываем пользователя к созданному курсу"""
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (IsAuthenticated, ~IsModerator,)
        elif self.action in ["update", "partial_update", "retrieve"]:
            self.permission_classes = (IsAuthenticated, IsModerator | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (IsAuthenticated, IsOwner,)
        return super().get_permissions()

    def get_queryset(self):
        if self.request.user.groups.filter(name="moders").exists():
            return super().get_queryset()
        else:
            return super().get_queryset().filter(owner=self.request.user)

    def perform_update(self, serializer):
        """
        Отправить сообщение об изменении курса всем подписанным абонентам
        :param serializer:
        :return:
        """
        course = serializer.save()
        course_id = course.id
        send_email_for_update_course.delay(course_id)


class LessonCreateApiView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModerator, IsAuthenticated)

    def perform_create(self, serializer):
        """Привязываем пользователя к созданному уроку"""
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListApiView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = LessonPagination

    def get_queryset(self):
        if self.request.user.groups.filter(name="moders").exists():
            return super().get_queryset()
        else:
            return super().get_queryset().filter(owner=self.request.user)


class LessonRetrieveApiView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModerator | IsOwner)


class LessonUpdateApiView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModerator | IsOwner)


class LessonDestroyApiView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwner | ~IsModerator)


class SubscriptionAPIView(APIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def post(self, *args, **kwargs):

        course = Course.objects.get(pk=self.kwargs["pk"])
        user = self.request.user
        subscription, created = Subscription.objects.get_or_create(course=course, owner=user)

        if subscription.status:
            subscription.status = False
            subscription.save()
            message = "Вы отписались от курса."
        else:
            subscription.status = True
            subscription.save()
            message = "Вы подписались на курс."

        return Response({"message": message})
