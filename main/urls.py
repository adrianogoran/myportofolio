from django.urls import path

from main.views import show_main, show_experience, show_achievements, create_experience, create_achievement, show_xml, show_json, show_xml_by_id, show_json_by_id, get_experience_json, delete_experience

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path('achievements/', show_achievements, name='show_achievements'),
    path('create-experience/', create_experience, name='create_experience'),
    path('create-achievement/', create_achievement, name='create_achievement'),

    path("xml/", show_xml, name="show_xml"),
    
    
    path("json/", get_experience_json, name="show_json"), 
    
    path("xml/<str:id>/", show_xml_by_id, name="show_xml_by_id"),
    path("json/<str:id>/", show_json_by_id, name="show_json_by_id"),

    path("api/experience/", get_experience_json, name="get_experience_json"),
    path('delete/<str:id>/', delete_experience, name='delete_experience'),
]