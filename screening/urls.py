from django.urls import path
from . import views

app_name = "screening"

urlpatterns = [
    path("", views.home, name="home"),
    path("screen/", views.screen_resumes, name="screen"),
    path("results/<int:session_id>/", views.results, name="results"),
    path("results/<int:session_id>/export/", views.export_csv, name="export_csv"),
]
