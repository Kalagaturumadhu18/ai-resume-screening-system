from django.contrib import admin
from .models import CandidateResult, ScreeningSession

class CandidateResultInline(admin.TabularInline):
    model = CandidateResult
    extra = 0
    readonly_fields = ("resume_name", "match_score", "matched_skills", "missing_skills")

@admin.register(ScreeningSession)
class ScreeningSessionAdmin(admin.ModelAdmin):
    list_display = ("role_title", "created_at")
    search_fields = ("role_title", "job_description")
    inlines = [CandidateResultInline]

@admin.register(CandidateResult)
class CandidateResultAdmin(admin.ModelAdmin):
    list_display = ("resume_name", "session", "match_score", "created_at")
    search_fields = ("resume_name",)
