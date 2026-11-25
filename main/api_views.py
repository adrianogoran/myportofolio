from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Achievement, Experience, Project
from main.permissions import (
    IsPortfolioOwnerOrEditorOrReadOnly, IsPortfolioOwnerOrReadOnly,
    IsProjectOwnerOrReadOnly,
)
from main.serializers import AchievementSerializer, ExperienceSerializer, ProjectSerializer


@api_view(["GET", "HEAD", "POST"])
@permission_classes([IsPortfolioOwnerOrReadOnly])
def experience_list(request):
    if request.method in ("GET", "HEAD"):
        experiences = Experience.objects.prefetch_related("starred_by").order_by("title")
        title = request.query_params.get("title", "").strip()
        if title:
            experiences = experiences.filter(title__icontains=title)
        serializer = ExperienceSerializer(
            experiences, many=True, context={"request": request},
        )
        return Response(serializer.data)

    serializer = ExperienceSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@permission_classes([IsPortfolioOwnerOrReadOnly])
def experience_detail(request, experience_id):
    experience = get_object_or_404(
        Experience.objects.prefetch_related("starred_by"), pk=experience_id,
    )
    if request.method in ("GET", "HEAD"):
        serializer = ExperienceSerializer(experience, context={"request": request})
        return Response(serializer.data)

    if request.method == "DELETE":
        experience.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = ExperienceSerializer(
        experience, data=request.data, partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def experience_star(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    if experience.starred_by.filter(pk=request.user.pk).exists():
        experience.starred_by.remove(request.user)
    else:
        experience.starred_by.add(request.user)
    serializer = ExperienceSerializer(experience, context={"request": request})
    return Response(serializer.data)


# ---------- Achievement ----------

@api_view(["GET", "HEAD", "POST"])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def achievement_list(request):
    """List achievements (optionally filtered with ?title=) or create one (owner only)."""
    if request.method in ("GET", "HEAD"):
        achievements = Achievement.objects.prefetch_related("starred_by").order_by("-date_awarded", "title")
        title = request.query_params.get("title", "").strip()
        if title:
            achievements = achievements.filter(title__icontains=title)
        serializer = AchievementSerializer(
            achievements, many=True, context={"request": request},
        )
        return Response(serializer.data)

    serializer = AchievementSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def achievement_detail(request, achievement_id):
    """Read, update (Editor or owner) or delete (owner only) a single achievement."""
    achievement = get_object_or_404(
        Achievement.objects.prefetch_related("starred_by"), pk=achievement_id,
    )
    if request.method in ("GET", "HEAD"):
        serializer = AchievementSerializer(achievement, context={"request": request})
        return Response(serializer.data)

    if request.method == "DELETE":
        achievement.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = AchievementSerializer(
        achievement, data=request.data, partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def achievement_star(request, achievement_id):
    """Toggle the logged-in user's star; the account always comes from request.user."""
    achievement = get_object_or_404(Achievement, pk=achievement_id)
    if achievement.starred_by.filter(pk=request.user.pk).exists():
        achievement.starred_by.remove(request.user)
    else:
        achievement.starred_by.add(request.user)
    serializer = AchievementSerializer(achievement, context={"request": request})
    return Response(serializer.data)


# ---------- Project ----------

@api_view(["GET", "HEAD", "POST"])
@permission_classes([IsProjectOwnerOrReadOnly])
def project_list(request):
    """List projects or create one (owner only)."""
    if request.method in ("GET", "HEAD"):
        projects = Project.objects.order_by("-created_at")
        return Response(ProjectSerializer(projects, many=True).data)

    serializer = ProjectSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD"])
def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return Response(ProjectSerializer(project).data)


# ---------- Authentication ----------

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_logout(request):
    """Revoke the token used for this request (None for session logins)."""
    if request.auth is not None:
        request.auth.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
