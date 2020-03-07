from django.views.generic import CreateView

from attendance.apps.course.forms import GenerateCodeForm


class GenerateCodeView(CreateView):
    template_name = 'course/code.html'
    form_class = GenerateCodeForm
