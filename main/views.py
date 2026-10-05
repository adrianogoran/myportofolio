from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse,JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from main.forms import ExperienceForm, AchievementForm
from main.models import Achievement, Experience
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
import datetime
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST



def show_main(request):
    last_login = request.COOKIES.get('last_login','No active login session / Cookie not found')
    context = {
        "name": "Goran",
        "npm": "2506558251",
        "study_program": "S1 Ilmu Komputer International",
        "bio": (
            "A Computer Science student at Universitas Indonesia interested "
            "in Data Science, Cybersecurity."
        ),
        "last_login" : last_login,
    }
    return render(request, "index.html", context)


# ---------- Experience ----------

def show_experience(request):
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Goran",
        "title_query": title_query,
        "form" : ExperienceForm(),
    }
    return render(request, "experience.html", context)

@login_required(login_url='/login/')
def create_experience(request):
    if not  request.user.is_superuser:
        raise PermissionDenied
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

@require_POST
def create_experience_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Only the portfolio owner can add experiences."},
            status=403,
        )

    form = ExperienceForm(request.POST)
    if form.is_valid():
        experience = form.save()
        return JsonResponse(
            {"message": "Experience added successfully.", "pk": str(experience.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

@login_required(login_url='/login/')
def edit_experience(request, id):
    if not request.user.has_perm("main.change_experience"):
        raise PermissionDenied
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

@login_required(login_url='/login/')
def delete_experience(request, id):
    if not request.user.is_superuser:
        raise PermissionDenied
    experience = get_object_or_404(Experience, pk=id)
    experience.delete()
    messages.success(request, "Experience successfully deleted!")
    return redirect("main:show_experience")


def get_experience_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.prefetch_related("starred_by").all()
    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    data = []
    for exp in experiences:
        starred_users = list(exp.starred_by.all())
        data.append({
            "pk": str(exp.id),
            "fields": {
                "title" : exp.title,
                "description" : exp.description,
                "category": exp.category,
                "thumbnail": exp.thumbnail,
                "started_at": exp.started_at,
                "ended_at": exp.ended_at,
                "star_count": len(starred_users),
                "is_starred": request.user.is_authenticated and request.user in starred_users,
                "starred_by_names": ", ".join(u.username for u in starred_users),
            }
        })
    return JsonResponse(data, safe=False)


# ---------- Achievement ----------

def show_achievements(request):

    context = {
        "name": "Goran",
        "title_query": request.GET.get("title","").strip(),
        "form" : AchievementForm(),
    }
    return render(request, "achievements.html", context)


@login_required(login_url='/login/')
def create_achievement(request):
    if not request.user.is_superuser:
        raise PermissionDenied
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

@require_POST
def create_achievement_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Only the portfolio owner can add achievements."},
            status=403,
        )

    form = AchievementForm(request.POST)
    if form.is_valid():
        achievement = form.save()
        return JsonResponse(
            {"message": "Achievement added successfully.", "pk": str(achievement.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

@login_required(login_url='/login/')
def edit_achievement(request, id):
    if not request.user.has_perm("main.change_achievement"):
        raise PermissionDenied
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


@login_required(login_url='/login/')
def delete_achievement(request, id):
    if not request.user.is_superuser:
        raise PermissionDenied
    achievement = get_object_or_404(Achievement, pk=id)
    if request.method == "POST":
        achievement.delete()
        messages.success(request, "Achievement successfully deleted!")
    return redirect("main:show_achievements")


def get_achievement_json(request):
    title_query = request.GET.get("title", "").strip()
    achievements = Achievement.objects.prefetch_related("starred_by").all()
    if title_query:
        achievements = achievements.filter(title__icontains=title_query)

    data = []
    for ach in achievements:
        starred_users = list(ach.starred_by.all())
        data.append({
            "pk": str(ach.id),
            "fields": {
                "title" : ach.title,
                "issuer" : ach.issuer,
                "category": ach.category,
                "date_awarded": ach.date_awarded,
                "is_featured": ach.is_featured,
                "created_at": ach.created_at,
                "star_count": len(starred_users),
                "description": ach.description,
                "category_label": ach.get_category_display(),
                "is_starred": request.user.is_authenticated and request.user in starred_users,
                "starred_by_names": ", ".join(u.username for u in starred_users),
            }
        })
    return JsonResponse(data, safe=False)


# ---------- Data delivery ----------

def show_xml(request):
    data = Experience.objects.all()
    return HttpResponse(serializers.serialize("xml", data, use_natural_foreign_keys=True), content_type="application/xml")


def show_json(request):
    data = Experience.objects.all()
    return HttpResponse(serializers.serialize("json", data, use_natural_foreign_keys=True), content_type="application/json")


def show_xml_by_id(request, id):
    data = Experience.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data, use_natural_foreign_keys=True), content_type="application/xml")


def show_json_by_id(request, id):
    data = Experience.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data, use_natural_foreign_keys=True), content_type="application/json")


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

# ---------- Authentication / Authorization ----------

def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Account created successfully!, Please log in")
        return redirect("main:login")
    context = {
        "name" : "Goran",
        "form" : form
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response
    context = {
        "name" : "Goran",
        "form" : form
    }
    return render(request,"login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

@login_required(login_url="/login/")
def toggle_star(request,experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        if request.user in experience.starred_by.all():
            experience.starred_by.remove(request.user)
        else:
            experience.starred_by.add(request.user)
    return redirect("main:show_experience")

@login_required(login_url="/login/")
def toggle_achievement_star(request, achievement_id):
    achievement = get_object_or_404(Achievement, pk=achievement_id)

    if request.method == "POST":
        if request.user in achievement.starred_by.all():
            achievement.starred_by.remove(request.user)
        else:
            achievement.starred_by.add(request.user)
    return redirect("main:show_achievements")
