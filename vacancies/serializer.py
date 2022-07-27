from rest_framework import serializers

from vacancies.models import Vacancy


class VacancySerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = Vacancy
        fields = ['id', 'text', 'slug', 'status', 'created', 'username']


class VacancyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = '__all__'