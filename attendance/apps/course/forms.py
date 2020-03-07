from django import forms

from attendance.apps.course.models import Code


class GenerateCodeForm(forms.ModelForm):
    class Meta:
        model = Code
        fields = ('group', )
