from django.urls import path
from rest_framework.authtoken import views as authtoken_views

from main import api_views

app_name = "api"

urlpatterns = [
    path("auth/token/", authtoken_views.obtain_auth_token, name="api_token_auth"),
    path("auth/logout/", api_views.api_logout, name="api_logout"),
    path("projects/", api_views.project_list, name="project-list"),
    path("projects/<uuid:project_id>/", api_views.project_detail, name="project-detail"),
    path("experiences/", api_views.experience_list, name="experience-list"),
    path("experiences/<uuid:experience_id>/", api_views.experience_detail, name="experience-detail"),
    path("experiences/<uuid:experience_id>/star/", api_views.experience_star, name="experience-star"),
    path("achievements/", api_views.achievement_list, name="achievement-list"),
    path("achievements/<uuid:achievement_id>/", api_views.achievement_detail, name="achievement-detail"),
    path("achievements/<uuid:achievement_id>/star/", api_views.achievement_star, name="achievement-star"),
]
