from django.shortcuts import render

from main.models import Experience


def show_main(request):
    context = {
        "name": "Goran",
        "npm": "2506558251",
        "study_program": "S1 Ilmu Komputer International",
        "bio": (
            "A Computer Science student at Universitas Indonesia interested "
            "in software development and education."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Goran",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)