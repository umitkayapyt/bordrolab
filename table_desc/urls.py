from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index , name='index'),
    path('process_salary_form/', views.process_salary_form, name='process_salary_form'),
    path('get-wage-params/<int:year>/', views.get_wage_params, name='get_wage_params'),
]
