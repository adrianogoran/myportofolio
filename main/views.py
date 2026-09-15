from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from main.forms import ExperienceForm, AchievementForm
from main.models import Achievement, Experience


def show_main(request):
    context = {
        "name": "Goran",
        "npm": "2506558251",
        "study_program": "S1 Ilmu Komputer International",
        "bio": (
            "A Computer Science student at Universitas Indonesia interested "
            "in Data Science, Cybersecurity."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    # Uses the JSON endpoint + deserialization and supports title filtering
    json_response = get_experience_json(request)

    experiences = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    experiences = [exp.object for exp in experiences]
    title_query = request.GET.get("title", "").strip()
    
    context = {
        "name": "Goran",
        "experience_list": experiences,
        "title_query": title_query,
    }
    return render(request, "experience.html", context)


def show_achievements(request):
    context = {
        "name": "Goran",
        "achievement_list": Achievement.objects.all(),
    }
    return render(request, "achievements.html", context)


def create_experience(request):
    form = ExperienceForm(request.POST or None)
    
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New experience successfully added!")
        return redirect("main:show_experience")
        
    context = {
        "name": "Goran",
        "form": form,
    }
    return render(request, "create_experience.html", context)


def delete_experience(request, id):
    experience = get_object_or_404(Experience, pk=id)
    experience.delete()
    messages.success(request, "Experience successfully deleted!")
    return redirect("main:show_experience")


def create_achievement(request):
    form = AchievementForm(request.POST or None)
    
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New achievement successfully added!")
        return redirect("main:show_achievements")
        
    context = {
        "name": "Goran",
        "form": form,
    }
    return render(request, "create_achievement.html", context)


def show_xml(request):
    data = Experience.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")


def show_json(request):
    data = Experience.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


def show_xml_by_id(request, id):
    data = Experience.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")


def show_json_by_id(request, id):
    data = Experience.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


def get_experience_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.all()
    if title_query:
        experiences = experiences.filter(title__icontains=title_query)
    
    experience_json = serializers.serialize("json", experiences)
    return HttpResponse(experience_json, content_type="application/json")