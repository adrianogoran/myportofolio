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
        self.assertContains(response, f'data-api-url="{reverse("api:experience-list")}"')
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

        # Cards are built by JavaScript, so the data is checked on the API.
        data = self.client.get(reverse("api:experience-list")).json()
        self.assertEqual(data[0]["title"], self.experience.title)
        self.assertEqual(data[0]["description"], self.experience.description)
        self.assertEqual(data[0]["category"], "part-time")
        self.assertIsNone(data[0]["ended_at"])

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "No experience has been added or found yet.")
        self.assertEqual(self.client.get(reverse("api:experience-list")).json(), [])

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        data = self.client.get(reverse("api:experience-list")).json()

        self.assertFalse(self.experience.is_ongoing)
        self.assertIsNotNone(data[0]["ended_at"])


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
        # Cards are built by JavaScript, so the data is checked on the API endpoint.
        fields = self.client.get(reverse("api:achievement-list")).json()[0]

        self.assertEqual(fields["title"], self.achievement.title)
        self.assertEqual(fields["issuer"], self.achievement.issuer)
        self.assertEqual(fields["description"], self.achievement.description)
        self.assertEqual(fields["category_label"], "Competition")
        self.assertEqual(fields["date_awarded"], "2026-07-01")

    def test_empty_achievements_page(self):
        Achievement.objects.all().delete()
        response = self.client.get(reverse("main:show_achievements"))

        self.assertContains(response, "No achievement has been added or found yet.")
        self.assertEqual(self.client.get(reverse("api:achievement-list")).json(), [])
