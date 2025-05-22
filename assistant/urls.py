from django.urls import path
from .views import index, analyze_symptoms, submit_feedback, signup_view, login_view, logout_view, home_view, \
    disease_detail_view, generate_report

urlpatterns = [
    path('', home_view, name='home'),  # Fixed function call
    path('index/',index, name='index'),
    path('analyze/', analyze_symptoms, name='analyze_symptoms'),
    path('disease/<str:disease_name>/', disease_detail_view, name='disease_detail'),
    path('generate-report/', generate_report, name='generate_report'),
    path("submit_feedback/", submit_feedback, name="submit_feedback"),
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]
