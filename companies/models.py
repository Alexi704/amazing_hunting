from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=40)
    logo = models.ImageField(upload_to='logos/')

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'
        # сортировка через модель рекомендована, если надо сортировать по умолчанию
        # знак "-" означает сортировку в обратном порядке, полей можно указывать сколько угодно
        # ordering = ["text", "-slug"]

    def __str__(self):
        return self.name
