from django import forms


class UploadFileForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        label="What is your name? 🤔",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    file = forms.FileField(
        label="Select your file ⬇️",
        widget=forms.ClearableFileInput(
            attrs={"class": "form-control", "accept": ".csv"}
        ),
    )
