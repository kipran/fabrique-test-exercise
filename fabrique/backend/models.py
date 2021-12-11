from django.db import models
from django.db.models.fields.related import ForeignKey

# Create your models here.
from django.utils.translation import gettext_lazy as _


class Survey(models.Model):
    name = models.CharField(max_length=100)
    date_starts = models.DateTimeField()
    date_ends = models.DateTimeField()
    description = models.TextField()


class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE,related_name='questions')

    question_text = models.TextField()
    
    required = models.BooleanField(default=False)

    question_order = models.SmallIntegerField()
    TEXT_ANSWER = "TEXT_ANSWER"
    ONE_CHOICE = "ONE_CHOICE"
    MULTIPLE_CHOICES = "MULTIPLE_CHOICES"

    QUESTION_TYPE_CHOICES = ((TEXT_ANSWER, _("Text answer")), (ONE_CHOICE, _(
        "One choice")), (MULTIPLE_CHOICES, _("Multiple choices")))

    question_type = models.CharField(
        max_length=20, choices=QUESTION_TYPE_CHOICES, verbose_name=_("Question type"))


class QuestionChoice(models.Model):
    question = models.ForeignKey(Question,related_name='question_choices', on_delete=models.CASCADE)
    choice_order = models.SmallIntegerField(blank=True)
    choice_text = models.TextField()
     


class UserSurveyForm(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    user_id = models.IntegerField()
    

class Answer(models.Model):
    user_form = ForeignKey(UserSurveyForm,related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    text = models.TextField(blank=True)

    choices = models.ManyToManyField(QuestionChoice, blank=True)
