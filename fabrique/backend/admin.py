from django.contrib import admin
from backend import models

admin.site.register(models.Question)
admin.site.register(models.QuestionChoice)
admin.site.register(models.Survey)
admin.site.register(models.UserSurveyForm)
admin.site.register(models.Answer)
# Register your models here.
