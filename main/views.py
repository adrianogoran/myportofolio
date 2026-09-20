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


# ---------- Experience ----------

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


def edit_experience(request, id):
    experience = get_object_or_404(Experience, pk=id)
    form = ExperienceForm(request.POST or None, instance=experience)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience successfully updated!")
        return redirect("main:show_experience")

    context = {
        "name": "Goran",
        "form": form,
        "experience": experience,
    }
    return render(request, "edit_experience.html", context)


def delete_experience(request, id):
    experience = get_object_or_404(Experience, pk=id)
    experience.delete()
    messages.success(request, "Experience successfully deleted!")
    return redirect("main:show_experience")


def get_experience_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.all()
    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    experience_json = serializers.serialize("json", experiences)
    return HttpResponse(experience_json, content_type="application/json")


# ---------- Achievement ----------

def show_achievements(request):
    """Mirrors show_experience: fetch JSON, then deserialize before rendering."""
    json_response = get_achievement_json(request)

    achievements = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    achievements = [ach.object for ach in achievements]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Goran",
        "achievement_list": achievements,
        "title_query": title_query,
    }
    return render(request, "achievements.html", context)


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


def delete_achievement(request, id):
    achievement = get_object_or_404(Achievement, pk=id)
    if request.method == "POST":
        achievement.delete()
        messages.success(request, "Achievement successfully deleted!")
    return redirect("main:show_achievements")


def get_achievement_json(request):
    title_query = request.GET.get("title", "").strip()
    achievements = Achievement.objects.all()
    if title_query:
        achievements = achievements.filter(title__icontains=title_query)

    achievement_json = serializers.serialize("json", achievements)
    return HttpResponse(achievement_json, content_type="application/json")


# ---------- Data delivery ----------

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


def show_achievement_xml(request):
    data = Achievement.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")


def show_achievement_json(request):
    data = Achievement.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


def show_achievement_xml_by_id(request, id):
    data = Achievement.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")


def show_achievement_json_by_id(request, id):
    data = Achievement.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def edit_achievement(request, id):
    achievement = get_object_or_404(Achievement, pk=id)
    form = AchievementForm(request.POST or None, instance=achievement)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Achievement successfully updated!")
        return redirect("main:show_achievements")

    context = {
        "name": "Goran",
        "form": form,
        "achievement": achievement,
    }
    return render(request, "edit_achievement.html", context)