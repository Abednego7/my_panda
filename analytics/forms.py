from django import forms


class UploadFileForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        label="What is your name? 🤔",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    opt_null = forms.ChoiceField(
        label="What do you want to do with null values? 🧮",
        choices=[
            ("nothing", "Do nothing"),
            ("delete", "Delete null data"),
            ("mean", "Replace with the mean"),
            ("median", "Replace with the median"),
            ("mode", "Replace with the mode"),
        ],
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    file = forms.FileField(
        label="Select your file ⬇️",
        widget=forms.ClearableFileInput(
            attrs={"class": "form-control", "accept": ".csv"}
        ),
    )
