import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from vacancies.models import Vacancy


def hello(request):
    result = """
                <div style='text-align:center; font-family:Georgia'>
                    <br/>
                    <h1>Привет!!!</h1>
                    <h2>Рад снова видеть тебя, мой друг!</h2>
                </div>
             """
    return HttpResponse(result)


@method_decorator(csrf_exempt, name='dispatch')
class VacancyView(View):
    def get(self, request):
        vacancies = Vacancy.objects.all()

        search_text = request.GET.get('s', None)
        if search_text:
            vacancies = vacancies.filter(text=search_text)

        response = []
        for vacancy in vacancies:
            response.append({'id': vacancy.id,
                             'text': vacancy.text, })
        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})

    def post(selfself, request):
        vacancy_data = json.loads(request.body)

        vacancy = Vacancy()
        vacancy.text = vacancy_data['text']

        vacancy.save()
        response = {'id': vacancy.id,
                    'text': vacancy.text, }
        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})


class VacancyDetailView(DetailView):
    model = Vacancy

    def get(self, request, *args, **kwargs):
        vacancy = self.get_object()

        response = {'id': vacancy.id,
                    'text': vacancy.text, }
        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})
