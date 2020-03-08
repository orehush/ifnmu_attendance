from django.urls.conf import path

from .views import GenerateCodeView, VerifyCodeView


urlpatterns = [
    path('code/generate', GenerateCodeView.as_view()),
    path('code/verify', VerifyCodeView.as_view()),
]
