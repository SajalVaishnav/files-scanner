from django.urls import path

from . import views

urlpatterns = [
    path('', views.SetSensKeywords.as_view()),
    path('success', views.KwSetSuccessfully.as_view()),
    path('get', views.GetSensKeywords.as_view()),
]