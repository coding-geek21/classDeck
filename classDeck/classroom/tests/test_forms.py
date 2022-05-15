from django.test import SimpleTestCase
from classroom.forms import *


class TestForms(SimpleTestCase):

    def test_question_form(self):
        form = QuestionForm(data={
            'text': 'What is 2+2 ?'
        })

        self.assertTrue(form.is_valid())

    def test_question_form_null(self):
        form = QuestionForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)