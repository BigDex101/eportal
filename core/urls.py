from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),   # 👈 homepage = login
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("results/<str:student_class>/<str:term>/", views.result_view, name="result"),
]