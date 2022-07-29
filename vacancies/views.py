from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count, Avg
from django.http import HttpResponse, JsonResponse
from django.views import View
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet

from amazing_hunting import settings
from vacancies.models import Vacancy, Skill
from vacancies.serializer import VacancyListSerializer, VacancyDetailSerializer, VacancyCreateSerializer, \
    VacancyUpdateSerializer, VacancyDestroySerializer, SkillSerializer


def hello(request):
    result = """<div style='text-align:center; font-family:Georgia'><br/>
                    <h1>Привет!!!</h1>
                    <h2>Рад снова видеть тебя, мой друг!</h2>
                </div>"""
    return HttpResponse(result)


class SkillsViewSet(ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class VacancyListView(ListAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyListSerializer

    def get(self, request, *args, **kwargs):
        vacancy_text = request.GET.get('text', None)
        if vacancy_text:
            self.queryset = self.queryset.filter(
                text__icontains=vacancy_text
            )

        skill_name = request.GET.get('skill', None)
        if skill_name:
            self.queryset = self.queryset.filter(
                skills__name__icontains=skill_name
            )

        return super().get(request, *args, **kwargs)


class VacancyDetailView(RetrieveAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyDetailSerializer


class VacancyCreateView(CreateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyCreateSerializer


class VacancyUpdateView(UpdateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyUpdateSerializer


class VacancyDeleteView(DestroyAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyDestroySerializer


class UserVacancyDetailView(View):
    def get(self, request):
        user_qs = User.objects.annotate(vacancies=Count('vacancy'))

        # пагинация
        paginator = Paginator(user_qs, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        users = []
        for user in page_obj:
            users.append({
                'id': user.id,
                'name': user.username,
                'vacancies': user.vacancies,
            })
        response = {
            'items': users,
            'total': paginator.count,
            'num_pages': paginator.num_pages,
            'avg': user_qs.aggregate(avg=Avg('vacancies'))['avg']
        }
        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})
