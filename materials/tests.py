from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User, Subscription
from .models import Course, Lesson


class LessonCRUDTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='user@example.com',
            username='user',
            password='TestPassword123!',
        )

        self.other_user = User.objects.create_user(
            email='other@example.com',
            username='other',
            password='TestPassword123!',
        )

        self.course = Course.objects.create(
            title='Test Course',
            description='Test description',
            owner=self.user,
        )

        self.lesson = Lesson.objects.create(
            course=self.course,
            title='Test Lesson',
            description='Test lesson description',
            video_url='https://youtube.com/watch?v=test',
            owner=self.user,
        )

    def test_lesson_list(self):
        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.get(
            reverse('lesson-list-create')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_create_lesson(self):
        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.post(
            reverse('lesson-list-create'),
            {
                'course': self.course.id,
                'title': 'New Lesson',
                'description': 'New lesson',
                'video_url': 'https://youtube.com/watch?v=test2',
            },
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            Lesson.objects.count(),
            2,
        )

    def test_update_own_lesson(self):
        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.patch(
            reverse(
                'lesson-detail',
                kwargs={'pk': self.lesson.id},
            ),
            {
                'title': 'Updated Lesson',
            },
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.lesson.refresh_from_db()

        self.assertEqual(
            self.lesson.title,
            'Updated Lesson',
        )

    def test_delete_own_lesson(self):
        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.delete(
            reverse(
                'lesson-detail',
                kwargs={'pk': self.lesson.id},
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Lesson.objects.filter(
                pk=self.lesson.id
            ).exists()
        )

    def test_other_user_cannot_update_lesson(self):
        self.client.force_authenticate(
            user=self.other_user
        )

        response = self.client.patch(
            reverse(
                'lesson-detail',
                kwargs={'pk': self.lesson.id},
            ),
            {
                'title': 'Hacked Lesson',
            },
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_other_user_cannot_delete_lesson(self):
        self.client.force_authenticate(
            user=self.other_user
        )

        response = self.client.delete(
            reverse(
                'lesson-detail',
                kwargs={'pk': self.lesson.id},
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )


class LessonValidatorTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='validator@example.com',
            username='validator',
            password='TestPassword123!',
        )

        self.course = Course.objects.create(
            title='Validator Course',
            owner=self.user,
        )

    def test_youtube_url_is_allowed(self):
        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.post(
            reverse('lesson-list-create'),
            {
                'course': self.course.id,
                'title': 'YouTube Lesson',
                'description': 'Test',
                'video_url': (
                    'https://www.youtube.com/watch?v=123'
                ),
            },
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_external_url_is_rejected(self):
        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.post(
            reverse('lesson-list-create'),
            {
                'course': self.course.id,
                'title': 'Bad Lesson',
                'description': 'Test',
                'video_url': 'https://example.com/video',
            },
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )


class SubscriptionTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='subscriber@example.com',
            username='subscriber',
            password='TestPassword123!',
        )

        self.course = Course.objects.create(
            title='Subscription Course',
            owner=self.user,
        )

        self.url = reverse('subscription-toggle')

    def test_subscribe_to_course(self):
        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.post(
            self.url,
            {
                'course_id': self.course.id,
            },
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            Subscription.objects.filter(
                user=self.user,
                course=self.course,
            ).exists()
        )

        self.assertEqual(
            response.data['is_subscribed'],
            True,
        )

    def test_unsubscribe_from_course(self):
        Subscription.objects.create(
            user=self.user,
            course=self.course,
        )

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.post(
            self.url,
            {
                'course_id': self.course.id,
            },
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertFalse(
            Subscription.objects.filter(
                user=self.user,
                course=self.course,
            ).exists()
        )

        self.assertEqual(
            response.data['is_subscribed'],
            False,
        )

    def test_course_contains_subscription_status(self):
        Subscription.objects.create(
            user=self.user,
            course=self.course,
        )

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.get(
            reverse(
                'course-detail',
                kwargs={'pk': self.course.id},
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            response.data['is_subscribed']
        )

    def test_subscription_requires_authentication(self):
        response = self.client.post(
            self.url,
            {
                'course_id': self.course.id,
            },
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )


class CoursePaginationTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='pagination@example.com',
            username='pagination',
            password='TestPassword123!',
        )

        Course.objects.bulk_create([
            Course(
                title=f'Course {i}',
                owner=self.user,
            )
            for i in range(12)
        ])

    def test_course_pagination(self):
        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.get(
            reverse('course-list')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data['results']),
            5,
        )

        self.assertIn(
            'next',
            response.data,
        )

        self.assertIn(
            'previous',
            response.data,
        )
