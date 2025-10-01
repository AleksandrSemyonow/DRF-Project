from rest_framework.test import APITestCase
from users.models import User
from materials.models import Course, Lesson, Subscription
from django.urls import reverse
from rest_framework import status


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@sky.com")
        self.course = Course.objects.create(title="Python", description="Python developer", owner=self.user)
        self.lesson = Lesson.objects.create(title="Django", description="DRF", course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        retrieve_url = reverse("materials:lessons_retrieve", args=[self.lesson.id])
        response = self.client.get(retrieve_url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data.get("title"), self.lesson.title)

    def test_lesson_create(self):
        create_url = reverse("materials:lessons_create")
        data = {
            "title": "test",
            "course": 1,
            "video_url": "https://www.youtube.com/",
            "description": "test description",
            "owner": self.user.id
        }
        response = self.client.post(create_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_lesson_update(self):
        update_url = reverse("materials:lessons_update", args=[self.lesson.id])
        data = {
            "title": "update title",
            "description": "update description"
        }
        response = self.client.patch(update_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.lesson.refresh_from_db()

        self.assertEqual(data.get("title"), self.lesson.title)

        self.assertEqual(data.get("description"), self.lesson.description)

    def test_lesson_delete(self):
        delete_url = reverse("materials:lessons_delete", args=[self.lesson.id])
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        list_url = reverse("materials:lessons_list")

        response = self.client.get(list_url)

        print(response.json())

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test2@sky.com")
        self.course = Course.objects.create(title="Java", description="Java developer", owner=self.user)
        self.subscription = Subscription.objects.create(owner=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)

    def test_sub_create(self):
        sub_url = reverse("materials:subscriptions", args=[self.course.id])
        response = self.client.post(sub_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Вы подписались на курс.")
