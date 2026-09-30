from django.forms import ModelForm, TextInput, Textarea, URLInput, Select, DateInput, DateTimeInput
from django.utils.html import strip_tags
from main.models import Experience, Achievement
from django.core.exceptions import ValidationError 

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = ["title", "description", "category", "thumbnail", "ended_at"]
        
        labels = {
            "title": "Experience Title",
            "description": "Description",
            "category": "Category",
            "thumbnail": "Thumbnail URL",
            "ended_at": "End Date (Optional)",
        }
        
        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "e.g., Software Engineering Intern",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Describe what you did...",
                    "rows": 3,
                }
            ),
            "category": Select(
                attrs={
                    "class": "form-select", 
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://example.com/image.png",
                }
            ),
            "ended_at": DateTimeInput(
                attrs={
                    "type": "datetime-local",
                }
            ),
        }

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Experience title can't contain only HTML tags.")
        return title

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()


class AchievementForm(ModelForm):
    class Meta:
        model = Achievement
        fields = ["title", "issuer", "description", "category", "date_awarded","is_featured"]
        
        labels = {
            "title": "Achievement Title",
            "issuer": "Issuer / Organization",
            "description": "Description",
            "category": "Category",
            "date_awarded": "Date Awarded",
        }
        
        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "e.g., 1st Place Hackathon",
                    "maxlength": 255,
                }
            ),
            "issuer": TextInput(
                attrs={
                    "placeholder": "e.g., Universitas Indonesia",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Tell us about this achievement...",
                    "rows": 3,
                }
            ),
            "category": Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "date_awarded": DateInput(
                attrs={
                    "type": "date",
                }
            ),
        }

    def clean_title(self):
        title = self.cleaned_data["title"]
        return strip_tags(title)

    def clean_issuer(self):
        issuer = self.cleaned_data["issuer"]
        return strip_tags(issuer)

    def clean_description(self):
        description = self.cleaned_data["description"]
        return strip_tags(description)
    