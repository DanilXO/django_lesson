import datetime

from django.urls import reverse
from django.utils import timezone
from django.test import TestCase

from polls.models import Question


class QuestionMethodTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertEqual(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently () должен возвращать False для вопросов, чьи
        pub_date старше 1 дня.
        """
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertFalse(old_question.was_published_recently())
        # self.assertEqual(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() должен вернуть True для вопросов, чьи
         pub_date в течение последнего дня.
        """
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(pub_date=time)
        self.assertTrue(recent_question.was_published_recently())
        # self.assertEqual(recent_question.was_published_recently(), True)