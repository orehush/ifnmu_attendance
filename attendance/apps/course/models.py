from datetime import timedelta
from django.conf import settings
from django.db import models
from django.utils import timezone

from attendance.apps.course.utils import generate_code


class Course(models.Model):
    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курси'

    name = models.CharField('Назва', max_length=250)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Власник курсу',
        on_delete=models.CASCADE,
    )
    is_active = models.BooleanField('Активний', default=True)

    def __str__(self):
        return self.name


class Group(models.Model):
    class Meta:
        verbose_name = 'Група'
        verbose_name_plural = 'Групи'

    name = models.CharField('Назва', max_length=250)
    course = models.ForeignKey(
        Course,
        verbose_name='Курс',
        on_delete=models.CASCADE,
    )
    start = models.TimeField('Початок заняття')
    end = models.TimeField('Кінець заняття')
    is_active = models.BooleanField('Активна', default=True)

    def __str__(self):
        return f'{self.course} - {self.name}'


class Code(models.Model):
    class Meta:
        verbose_name = 'Код верифікації'
        verbose_name_plural = 'Коди верифікації'

    group = models.ForeignKey(
        Group,
        verbose_name='Група',
        on_delete=models.CASCADE
    )
    value = models.CharField(max_length=10, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    expired_at = models.DateTimeField(editable=False)

    def save(self, **kwargs):
        if not self.pk:
            self.value = generate_code()
            self.expired_at = timezone.now() + timedelta(
                seconds=settings.CODE_VERIFICATION_SECONDS
            )
        super(Code, self).save(**kwargs)

    def __str__(self):
        return self.value


class Attendance(models.Model):
    class Meta:
        verbose_name = 'Присутність студента'
        verbose_name_plural = 'Журнал відвідуваності'

    group = models.ForeignKey(
        Group,
        verbose_name='Група',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Студент',
        on_delete=models.CASCADE
    )
    code = models.ForeignKey(
        Code,
        verbose_name='Код верифікації',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
