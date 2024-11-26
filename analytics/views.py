from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views import View
from .forms import UploadFileForm

# Pandas
import pandas as pd


# Create your views here.
class HomeView(View):
    def get(self, request):
        form = UploadFileForm()
        return render(request, "analytics/home.html", {"form": form})

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            name = request.POST["name"]
            csv_file = request.FILES["file"]
            print(f"persona: {name}\narchivo: {csv_file}")

            if not csv_file.name.endswith(".csv"):
                return HttpResponseBadRequest("The file you uploaded is not a csv file")

            try:
                df = pd.read_csv(csv_file)
            except Exception as e:
                return HttpResponseBadRequest(f"Error reading file: {e}")

            # Details
            columns = df.columns.tolist()
            values = df.values.tolist()
            counts = df.count().tolist()
            data_frame_info = {key: count for key, count in zip(columns, counts)}

            data_frame_context = {
                "columns": columns,
                "values": values,
                "total_rows": data_frame_info,
            }

            # "form": form -> To load valid form after submitting it
            return render(
                request,
                "analytics/home.html",
                {"form": form, "name": name, "dataframe": data_frame_context},
            )

        # To reload invalid form
        return render(request, "analytics/home.html", {"form": form})
