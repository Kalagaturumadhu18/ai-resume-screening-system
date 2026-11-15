from django.db import models

class ScreeningSession(models.Model):
    role_title = models.CharField(max_length=150)
    job_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.role_title} ({self.created_at:%Y-%m-%d %H:%M})"


class CandidateResult(models.Model):
    session = models.ForeignKey(
        ScreeningSession, related_name="candidates", on_delete=models.CASCADE
    )
    resume_name = models.CharField(max_length=255)
    extracted_text = models.TextField(blank=True)
    match_score = models.FloatField(default=0)
    matched_skills = models.JSONField(default=list, blank=True)
    missing_skills = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-match_score", "resume_name"]

    def __str__(self):
        return f"{self.resume_name} - {self.match_score:.1f}%"
