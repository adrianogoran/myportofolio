from django.urls import path
from main.views import (
    show_main,
    show_experience,
    create_experience,
    edit_experience,
    delete_experience,
    get_experience_json,
    show_achievements,
    create_achievement,
    delete_achievement,
    get_achievement_json,
    show_xml,
    show_json,
    show_xml_by_id,
    show_json_by_id,
    show_achievement_xml,
    show_achievement_json,
    show_achievement_xml_by_id,
    show_achievement_json_by_id,
    edit_achievement,
    register,
    login_user,
    logout_user,
    toggle_star,
)
app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),

    # --- Experience ---
    path("experience/", show_experience, name="show_experience"),
    path("create-experience/", create_experience, name="create_experience"),
    path("edit-experience/<str:id>/", edit_experience, name="edit_experience"),
    path("delete/<str:id>/", delete_experience, name="delete_experience"),

    # --- Achievement ---
    path("achievements/", show_achievements, name="show_achievements"),
    path("create-achievement/", create_achievement, name="create_achievement"),
    path("delete-achievement/<str:id>/", delete_achievement, name="delete_achievement"),

        # --- Data delivery: Achievement ---
    path("xml/achievements/", show_achievement_xml, name="show_achievement_xml"),
    path("json/achievements/", show_achievement_json, name="show_achievement_json"),
    path("xml/achievements/<str:id>/", show_achievement_xml_by_id, name="show_achievement_xml_by_id"),
    path("json/achievements/<str:id>/", show_achievement_json_by_id, name="show_achievement_json_by_id"),
    path("api/achievements/", get_achievement_json, name="get_achievement_json"),
    path("edit-achievement/<str:id>/", edit_achievement, name="edit_achievement"),

    # --- Data delivery: Experience ---
    path("xml/", show_xml, name="show_xml"),
    path("json/", show_json, name="show_json"),
    path("xml/<str:id>/", show_xml_by_id, name="show_xml_by_id"),
    path("json/<str:id>/", show_json_by_id, name="show_json_by_id"),
    path("api/experience/", get_experience_json, name="get_experience_json"),

    # --- Auth ---
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("experience/<uuid:experience_id>/star/", toggle_star, name="toggle_star"),
]