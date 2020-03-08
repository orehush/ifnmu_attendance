from django import forms
from django.db.models import Q
from django.db.models.functions.datetime import TruncDate
from django.utils import timezone
from django_select2.forms import Select2Widget

from attendance.apps.course.models import Code, Attendance


class GenerateCodeForm(forms.ModelForm):
    class Meta:
        model = Code
        fields = ('group', )
        widgets = {
            'group': Select2Widget()
        }


class VerifyCodeForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ('code', )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(VerifyCodeForm, self).__init__(*args, **kwargs)

    code = forms.CharField(
        label='Код курсу',
        help_text='Код генерує викладач і повідомляє групі',
        max_length=5,
        required=True,
    )

    def clean_code(self):
        value = self.cleaned_data['code']
        now = timezone.localtime()
        time = now.time()
        try:
            code = Code.objects.filter(expired_at__gte=now).get(value=value.upper())
        except (Code.DoesNotExist, Code.MultipleObjectsReturned) as e:
            raise forms.ValidationError(
                'Код невалідний або вигас. '
                'Попросіть викладача зненерувати новий код'
            )
        group = code.group
        if not group.is_active:
            raise forms.ValidationError('Група більше не активна в цьому курсі')
        if not group.course.is_active:
            raise forms.ValidationError('Курс більше не активний')
        if not (group.start <= time <= group.end):
            raise forms.ValidationError('Група недоступна в цей час')
        if Attendance.objects.annotate(date=TruncDate('created_at')).filter(
            Q(code=code) | Q(group=code.group, date=now.date()),
            user=self.user,
        ).exists():
            raise forms.ValidationError('Ви вже відмічені в цій групі сьогодні')
        return code

    def save(self, commit=True):
        code = self.cleaned_data['code']  # type: Code
        group = code.group
        return Attendance.objects.create(code=code, group=group, user=self.user)
