from django.urls.conf import path

from .views import GenerateCodeView


urlpatterns = [
    path('generate', GenerateCodeView.as_view()),
]
