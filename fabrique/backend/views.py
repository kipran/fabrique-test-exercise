
from django.shortcuts import render

from rest_framework import generics
from rest_framework.views import APIView
from backend import models

from backend import serializers

from django.http import Http404

from rest_framework.response import Response

from rest_framework import authentication, permissions

class SurveyDetailedView(generics.RetrieveAPIView):
    queryset = models.Survey.objects.all()
    serializer_class = serializers.SurveyNestedReadSerializer


class SurveyListView(generics.ListAPIView):
    queryset = models.Survey.objects.all()
    serializer_class = serializers.SurveySerializer

class UserSurveyFormListView(generics.ListAPIView):
    
    serializer_class = serializers.UserSurveyFormSerializer
    def get_queryset(self):
        
        user = self.kwargs['user_id']
        return models.UserSurveyForm.objects.filter(user_id=user)

class UserSurveyFormDetailedView(APIView):
    
    def get_object(self, survey_id, user_id ):
        try:
            return models.UserSurveyForm.objects.get(survey=survey_id,user_id=user_id)
        except models.UserSurveyForm.DoesNotExist:
            raise Http404

    def get(self,request,survey_id, user_id, format=None):
        user_form = self.get_object(survey_id,user_id)
        serializer = serializers.UserSurveyFormNestedReadSerializer(user_form)
        return Response(serializer.data)


class UserSurveyFormCreate(generics.CreateAPIView):
    queryset = models.UserSurveyForm.objects.all()
    serializer_class = serializers.UserSurveyFormNestedCreateSerializer
    
#admin views below
class AdminSurveyCreate(generics.CreateAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = models.Survey.objects.all()
    serializer_class = serializers.SurveyNestedCreateSerializer

class AdminSurveyDelete(generics.DestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = models.Survey.objects.all()

class AdminSurveyUpdate(generics.UpdateAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = models.Survey.objects.all()
    serializer_class = serializers.SurveySerializer

class AdminQuestionDelete(generics.DestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = models.Question.objects.all()

class AdminQuestionCreate(generics.CreateAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionNestedCreateSerializer

class AdminQuestionUpdate(generics.UpdateAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionSerializer

class AdminQuestionChoiceUpdate(generics.UpdateAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = models.QuestionChoice.objects.all()
    serializer_class = serializers.QuestionChoiceCreateUpdateSerializer

class AdminQuestionChoiceDelete(generics.DestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = models.QuestionChoice.objects.all()

class AdminQuestionChoiceCreate(generics.CreateAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = models.QuestionChoice.objects.all()
    serializer_class = serializers.QuestionChoiceCreateUpdateSerializer


# Create your views here.
