from challenge import views
from django.urls import path

urlpatterns = [
    path('', views.home_file_upload, name="home"),
    path('result', views.display_result, name="result"),
    path('getall', views.forexApi, name="getall"),
]
