import csv
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST

from .forms import ResumeScreeningForm
from .models import CandidateResult, ScreeningSession
from .services import analyze_resume, extract_pdf_text


@require_GET
def home(request):
    recent_sessions = ScreeningSession.objects.all()[:5]
    return render(request, "screening/home.html", {
        "form": ResumeScreeningForm(),
        "recent_sessions": recent_sessions,
    })


@require_POST
def screen_resumes(request):
    form = ResumeScreeningForm(request.POST, request.FILES)
    if not form.is_valid():
        return render(request, "screening/home.html", {
            "form": form,
            "recent_sessions": ScreeningSession.objects.all()[:5],
        }, status=400)

    role_title = form.cleaned_data["role_title"]
    job_description = form.cleaned_data["job_description"]
    session = ScreeningSession.objects.create(
        role_title=role_title,
        job_description=job_description,
    )

    processed = 0
    errors = []
    for uploaded in form.cleaned_data["resumes"]:
        try:
            resume_text = extract_pdf_text(uploaded)
            analysis = analyze_resume(job_description, resume_text)
            CandidateResult.objects.create(
                session=session,
                resume_name=uploaded.name,
                extracted_text=resume_text[:50000],
                match_score=analysis["score"],
                matched_skills=analysis["matched_skills"],
                missing_skills=analysis["missing_skills"],
            )
            processed += 1
        except Exception as exc:
            errors.append(f"{uploaded.name}: {str(exc)}")

    if processed == 0:
        session.delete()
        form.add_error(None, "No resumes could be processed. " + " | ".join(errors))
        return render(request, "screening/home.html", {
            "form": form,
            "recent_sessions": ScreeningSession.objects.all()[:5],
        }, status=400)

    if errors:
        messages.warning(request, "Some files could not be processed: " + " | ".join(errors))
    messages.success(request, f"Successfully screened {processed} resume(s).")
    return redirect("screening:results", session_id=session.id)


@require_GET
def results(request, session_id):
    session = get_object_or_404(ScreeningSession, id=session_id)
    candidates = session.candidates.all()
    return render(request, "screening/results.html", {
        "session": session,
        "candidates": candidates,
    })


@require_GET
def export_csv(request, session_id):
    session = get_object_or_404(ScreeningSession, id=session_id)
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        f'attachment; filename="screening-session-{session.id}.csv"'
    )
    writer = csv.writer(response)
    writer.writerow([
        "Resume", "Similarity score (%)", "Matched skills", "Skills in job description not detected"
    ])
    for candidate in session.candidates.all():
        writer.writerow([
            candidate.resume_name,
            candidate.match_score,
            ", ".join(candidate.matched_skills),
            ", ".join(candidate.missing_skills),
        ])
    return response
