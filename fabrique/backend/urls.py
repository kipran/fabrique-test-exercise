from django.urls import path
from backend import views

urlpatterns = [
    path('survey_list/', views.SurveyListView.as_view()),
    path('survey_list/<int:pk>/',views.SurveyDetailedView.as_view()),

    path('user_form_list/<int:user_id>/',views.UserSurveyFormListView.as_view()),
    path('user_form_list/<int:user_id>/<int:survey_id>/',views.UserSurveyFormDetailedView.as_view()),
    path('user_form_create/',views.UserSurveyFormCreate.as_view()),

    path('survey_create/',views.AdminSurveyCreate.as_view()),
    path('survey_delete/<int:pk>/',views.AdminSurveyDelete.as_view()),
    path('survey_update/<int:pk>/',views.AdminSurveyUpdate.as_view()),

    path('question_create/',views.AdminQuestionCreate.as_view()),
    path('question_delete/<int:pk>/',views.AdminQuestionDelete.as_view()),
    path('question_update/<int:pk>/',views.AdminQuestionUpdate.as_view()),

    path('question_choice_create/',views.AdminQuestionChoiceCreate.as_view()),
    path('question_choice_delete/<int:pk>/',views.AdminQuestionChoiceDelete.as_view()),
    path('question_choice_update/<int:pk>/',views.AdminQuestionChoiceUpdate.as_view())

]