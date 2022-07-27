from rest_framework import serializers

from vacancies.models import Vacancy


class VacancyListSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    skills = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Vacancy
        fields = ['id', 'text', 'slug', 'status', 'created', 'username', 'skills']


class VacancyDetailSerializer(serializers.ModelSerializer):
    skills = serializers.SlugRelatedField(many=True,
                                          read_only=True,
                                          slug_field='name')

    class Meta:
        model = Vacancy
        fields = '__all__'


class VacancyCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Vacancy
        exclude = ['skills']