from Homepage.models import Lecture
from django.contrib.auth.models import User
from django.shortcuts import render
from django.test import TestCase

class HomePageTest(TestCase):

    def test_saving_and_retrieving_lecture_title(self):
        firstLecture = Lecture()
        firstLecture.title = 'The first (ever) lecture title'
        firstLecture.save()

        secondLecture = Lecture()
        secondLecture.title = 'lecture title the second'
        secondLecture.save()

        lectures = Lecture.objects.all()
        self.assertEqual(lectures.count(), 2)

        firstLecture = lectures[0]
        secondLecture = lectures[1]
        self.assertEqual(firstLecture.title, 'The first (ever) lecture title')
        self.assertEqual(firstLecture.id, 1)
        self.assertEqual(secondLecture.title, 'lecture title the second')
        self.assertEqual(secondLecture.id, 2)

    def test_saving_lecture_id_auto_increment_start_at_1(self):
        firstLecture = Lecture()
        firstLecture.title = 'The first (ever) lecture title'
        firstLecture.save()

        secondLecture = Lecture()
        secondLecture.title = 'lecture title the second'
        secondLecture.save()

        lectures = Lecture.objects.all()
        self.assertEqual(lectures.count(), 2)

        firstLecture = lectures[0]
        secondLecture = lectures[1]
        self.assertEqual(firstLecture.id, 1)
        self.assertEqual(secondLecture.id, 2)

