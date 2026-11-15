
from django import forms


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean

        if isinstance(data, (list, tuple)):
            return [single_file_clean(item, initial) for item in data]

        return [single_file_clean(data, initial)]


class ResumeScreeningForm(forms.Form):
    role_title = forms.CharField(
        label="Job role",
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "e.g. Python Developer"})
    )

    job_description = forms.CharField(
        label="Job description",
        widget=forms.Textarea(attrs={"rows": 6})
    )

    resumes = MultipleFileField(
        label="PDF resumes",
        widget=MultipleFileInput(
            attrs={"multiple": True, "accept": ".pdf,application/pdf"}
        ),
        required=True,
    )
