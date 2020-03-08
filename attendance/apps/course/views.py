from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView


from attendance.apps.course.forms import GenerateCodeForm, VerifyCodeForm


class GenerateCodeView(PermissionRequiredMixin, CreateView):
    template_name = 'course/code.html'
    form_class = GenerateCodeForm
    permission_required = ('course.add_code', )

    def form_valid(self, form):
        code = form.save()
        context = self.get_context_data(code=code)
        return self.render_to_response(context)


class VerifyCodeView(LoginRequiredMixin, CreateView):
    template_name = 'course/verify_code.html'
    form_class = VerifyCodeForm

    def get_form_kwargs(self):
        kwargs = super(VerifyCodeView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        messages.success(
            self.request,
            'Ви успішно записані на курс: "%s"' % self.object.group
        )
        return self.render_to_response(self.get_context_data())
