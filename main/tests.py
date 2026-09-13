from datetime import date

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Achievement, Experience


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="PBP Teaching Assistant",
            description="Help students understand web development.",
            category="part-time",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/a-page-that-does-not-exist/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "PBP Teaching Assistant")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Ongoing")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "No experience has been added yet.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Completed")
        self.assertNotContains(response, "Ongoing")


class AchievementTest(TestCase):
    def setUp(self):
        self.achievement = Achievement.objects.create(
            title="Top 100 in Hackathon Digital Cooperatives",
            issuer="University of Indonesia",
            category="competition",
            date_awarded=date(2026, 7, 1),
            description="Qualified to the national top 100.",
        )

    def test_achievements_url_is_accessible(self):
        response = self.client.get(reverse("main:show_achievements"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "achievements.html")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_achievement_model(self):
        self.assertEqual(self.achievement.category, "competition")
        self.assertEqual(self.achievement.date_awarded, date(2026, 7, 1))

    def test_achievements_page_shows_data(self):
        response = self.client.get(reverse("main:show_achievements"))

        self.assertContains(response, self.achievement.title)
        self.assertContains(response, self.achievement.issuer)
        self.assertContains(response, self.achievement.description)
        self.assertContains(response, "Competition")
        self.assertContains(response, "Jul 2026")

    def test_empty_achievements_page(self):
        Achievement.objects.all().delete()
        response = self.client.get(reverse("main:show_achievements"))

        self.assertContains(response, "No achievements have been added yet.")