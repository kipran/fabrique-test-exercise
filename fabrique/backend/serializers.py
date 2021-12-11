from rest_framework import serializers
from backend import models

from rest_framework import validators


class QuestionChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuestionChoice
        fields = ['id', 'choice_order', 'choice_text']

class QuestionChoiceCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuestionChoice
        fields = ['id', 'choice_order', 'choice_text','question']

class QuestionNestedSerializer(serializers.ModelSerializer):
    question_choices = QuestionChoiceSerializer(many=True)

    class Meta:
        model = models.Question
        fields = ['id', 'question_type', 'required',
                  'question_text', 'question_order', 'question_choices']

    def create(self, validated_data):
        question_choices = validated_data.pop('question_choices')
        print(question_choices)

        question = models.Question.objects.create(**validated_data)

        for question_choice in question_choices:
            print(question_choice)
            choice_text = question_choice.pop("choice_text")
            choice_order = question_choice.pop("choice_order")
            print(choice_order)
            print(choice_text)
            question_choice_instance = models.QuestionChoice.objects.create(
                question=question, choice_text=choice_text, choice_order=choice_order)

        return question

class QuestionNestedCreateSerializer(serializers.ModelSerializer):

    question_choices = QuestionChoiceSerializer(many=True)

    class Meta:
        model = models.Question
        fields = ['id', 'question_type', 'required',
                  'question_text', 'question_order', 'question_choices','survey']

    def create(self, validated_data):
        question_choices = validated_data.pop('question_choices')
        print(question_choices)

        question = models.Question.objects.create(**validated_data)

        for question_choice in question_choices:
            print(question_choice)
            choice_text = question_choice.pop("choice_text")
            choice_order = question_choice.pop("choice_order")
            print(choice_order)
            print(choice_text)
            question_choice_instance = models.QuestionChoice.objects.create(
                question=question, choice_text=choice_text, choice_order=choice_order)

        return question

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = ['id', 'question_type', 'required',
                  'question_text', 'question_order']


class SurveyNestedReadSerializer(serializers.ModelSerializer):
    questions = QuestionNestedSerializer(many=True, read_only=True)

    class Meta:
        model = models.Survey
        fields = ['id', 'name', 'date_starts',
                  'date_ends', 'description', 'questions']


class SurveyNestedCreateSerializer(serializers.ModelSerializer):
    questions = QuestionNestedSerializer(many=True)

    class Meta:
        model = models.Survey
        fields = ['id', 'name', 'date_starts',
                  'date_ends', 'description', 'questions']

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        print(questions_data)

        survey = models.Survey.objects.create(**validated_data)

        for question_data in questions_data:
            question_type = question_data.pop("question_type")
            required = question_data.pop("required")
            question_text = question_data.pop("question_text")

            question_order = question_data.pop("question_order")
            question_choices = question_data.pop("question_choices")

            question = models.Question.objects.create(survey=survey, question_type=question_type, required=required, question_text=question_text,
                                                      question_order=question_order)

            if question_choices:
                print("QUESTION CHOICES NOT EMPTY")
                print(question_choices)
                for question_choice in question_choices:
                    print(question_choice)
                    choice_text = question_choice.pop("choice_text")
                    choice_order = question_choice.pop("choice_order")
                    print(choice_order)
                    print(choice_text)
                    question_choice_instance = models.QuestionChoice.objects.create(
                        question=question, choice_text=choice_text, choice_order=choice_order)

        return survey


# Survey serializer without nested fields
class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Survey
        fields = ['id', 'name', 'date_ends', 'description']
        read_only_fields = ['date_starts']

# Answers and Survey read serializers with nested fields

class AnswerNestedReadSerializer(serializers.ModelSerializer):
    question = serializers.SlugRelatedField(
        read_only=True, slug_field='question_text')
    choices = QuestionChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = models.Answer
        fields = ['question', 'text', 'choices']


class UserSurveyFormNestedReadSerializer(serializers.ModelSerializer):

    answers = AnswerNestedReadSerializer(many=True, read_only=True)

    class Meta:
        model = models.UserSurveyForm
        fields = ['id', 'survey', 'user_id', 'answers']


# Answers and Survey create serializers with nested fields

class AnswerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = ['question', 'text', 'choices']


class UserSurveyFormNestedCreateSerializer(serializers.ModelSerializer):
    answers = AnswerCreateSerializer(many=True)

    class Meta:
        model = models.UserSurveyForm
        fields = ['survey', 'user_id', 'answers']

    validators = [
        validators.UniqueTogetherValidator(
            queryset=models.UserSurveyForm.objects.all(),
            fields=['survey', 'user_id']
        )
    ]

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        print(answers_data)

        user_form = models.UserSurveyForm.objects.create(**validated_data)

        for answer_data in answers_data:
            text_data = answer_data.pop('text')
            question_data = answer_data.pop('question')
            answer = models.Answer.objects.create(
                text=text_data, question=question_data, user_form=user_form)

            choices = answer_data.pop('choices')
            for choice in choices:
                answer.choices.add(choice)

        return user_form


class UserSurveyFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserSurveyForm
        fields = ['id', 'survey']
