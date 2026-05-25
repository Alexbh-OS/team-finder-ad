from django.urls import path

from projects import views

app_name = "projects"

urlpatterns = [
    path("list/", views.project_list, name="list"),
    path("create-project/", views.project_create, name="create"),
    path("<int:pk>/", views.project_detail, name="detail"),
    path("<int:pk>/edit/", views.project_edit, name="edit"),
    path("join/<int:pk>/", views.join_project, name="join"),
    path("<int:pk>/toggle-status/", views.toggle_project_status, name="toggle_status"),
    path("<int:pk>/toggle-favorite/", views.toggle_favorite, name="toggle_favorite"),
    path("skill/autocomplete/", views.skill_autocomplete, name="skill_autocomplete"),
    path("<int:pk>/add-skill/", views.add_skill_to_project, name="add_skill"),
    path("<int:pk>/remove-skill/", views.remove_skill_from_project, name="remove_skill"),
]

