from django.urls import path
from . import views

urlpatterns = [
    path('student-form/', views.student_form, name='student_form'),
    path('student-rank/', views.student_rank, name='student_rank'),
    path('success_page/', views.success_page, name='success_page'),
]
