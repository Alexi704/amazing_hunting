import json

from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from vacancies.models import Vacancy, Skill


def hello(request):
    result = """
                <div style='text-align:center; font-family:Georgia'>
                    <br/>
                    <h1>Привет!!!</h1>
                    <h2>Рад снова видеть тебя, мой друг!</h2>
                </div>
             """
    return HttpResponse(result)


class VacancyListView(ListView):
    model = Vacancy

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        search_text = request.GET.get('s', None)
        if search_text:
            self.object_list = self.object_list.filter(text=search_text)

        response = []
        for vacancy in self.object_list:
            response.append({'id': vacancy.id,
                             'text': vacancy.text,
                             'slug': vacancy.slug,
                             'status': vacancy.status,
                             'created': vacancy.created,
                             'user': vacancy.user_id, })
        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})


class VacancyDetailView(DetailView):
    model = Vacancy

    def get(self, request, *args, **kwargs):
        vacancy = self.get_object()

        response = {'id': vacancy.id,
                    'text': vacancy.text,
                    'slug': vacancy.slug,
                    'status': vacancy.status,
                    'created': vacancy.created,
                    'user': vacancy.user_id, }
        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name='dispatch')
class VacancyCreateView(CreateView):
    model = Vacancy
    fields = ['user', 'slug', 'text', 'status', 'created', 'skills']

    def post(selfself, request, *args, **kwargs):
        vacancy_data = json.loads(request.body)

        vacancy = Vacancy.objects.create(
            user_id=vacancy_data['user_id'],
            slug=vacancy_data['slug'],
            text=vacancy_data['text'],
            status=vacancy_data['status'],
        )

        response = {'id': vacancy.id,
                    'text': vacancy.text,
                    'slug': vacancy.slug,
                    'status': vacancy.status,
                    'created': vacancy.created,
                    'user': vacancy.user_id, }
        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name='dispatch')
class VacancyUpdateView(UpdateView):
    model = Vacancy
    fields = ['slug', 'text', 'status', 'skills']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        vacancy_data = json.loads(request.body)

        self.object.slug = vacancy_data['slug']
        self.object.text = vacancy_data['text']
        self.object.status = vacancy_data['status']

        for skill in vacancy_data['skills']:
            try:
                skill_odj = Skill.objects.get(name=skill)
            except Skill.DoesNotExist:
                return JsonResponse({"error": "Skill not found"}, status=404)
            self.object.skills.add(skill_odj)

        self.object.save()

        response = {'id': self.object.id,
                    'user': self.object.user_id,
                    'slug': self.object.slug,
                    'text': self.object.text,
                    'status': self.object.status,

                    # т.к. мы обращаемся к полю дополнительно связанной таблицы типа many2many,
                    # то используем сл. конструкцию для вывода скилов
                    'skills': list(self.object.skills.all().values_list('name', flat=True)),
                    }
        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name='dispatch')
class VacancyDeleteView(DeleteView):
    model = Vacancy
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({'status': 'ok'}, status=200)
