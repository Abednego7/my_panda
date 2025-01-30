from django.core.paginator import Paginator
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render
from django.views import View
from .forms import UploadFileForm
from django.conf import settings

# Others -> Graphs
import base64
from io import BytesIO

# Pandas
import pandas as pd

# To work with files directly with json
from io import StringIO

# To work with the system
from os import path, makedirs, remove

import matplotlib

matplotlib.use("Agg")

# Seaborn
import seaborn as sns
import matplotlib.pyplot as plt


# Create your views here.
class HomeView(View):
    def get(self, request):
        name = request.session.get("name")
        # We retrieve the dataframe key stored in SESSIONS
        df_json = request.session.get("dataframe")

        if df_json:
            df = pd.read_json(StringIO(df_json))
            context = self._prepare_context(df, name)

            return render(request, "analytics/home.html", context)
        else:
            return render(request, "analytics/home.html", {"form": UploadFileForm()})

    def post(self, request):
        # Check if the user is requesting the file download
        if "download" in request.POST:
            return self._download_file(request)

        # If not, process the file upload
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            name = request.POST["name"]
            opt_null = request.POST["opt_null"]
            csv_file = request.FILES["file"]
            print(f"persona: {name}\nopcion: {opt_null}\narchivo: {csv_file}")

            if not csv_file.name.endswith(".csv"):
                return HttpResponseBadRequest("The file you uploaded is not a csv file")

            try:
                df = pd.read_csv(csv_file)
            except Exception as e:
                return HttpResponseBadRequest(f"Error reading file: {e}")

            # Handle null values
            self._handle_null_values(df, opt_null)

            # Save the clean file
            self._save_file(df)

            # Save the dataframe in SESSIONS
            request.session["name"] = name
            request.session["dataframe"] = df.to_json()

            # Preparing the context
            context = self._prepare_context(df, name)

            return render(request, "analytics/home.html", context)

        # Reload the form if it is not valid
        return render(request, "analytics/home.html", {"form": form})

    def _handle_null_values(self, df, opt_null):
        match opt_null:
            case "delete":
                df.dropna(inplace=True)
            case "mean":
                for col in df.columns:
                    if df[col].dtype in ["int64", "float64"]:
                        df[col] = df[col].fillna(df[col].mean())
            case "median":
                for col in df.columns:
                    if df[col].dtype in ["int64", "float64"]:
                        df[col] = df[col].fillna(df[col].median())
            case "mode":
                for col in df.columns:
                    if df[col].dtype in ["int64", "float64"]:
                        df[col] = df[col].fillna(df[col].mode()[0])
            case _:
                pass

    def _save_file(self, df):
        media_path = path.join(settings.MEDIA_ROOT, "clean_file.csv")

        # Create the directory if it does not exist
        makedirs(settings.MEDIA_ROOT, exist_ok=True)

        df.to_csv(media_path, index=False)

        return media_path

    def _download_file(self, request):
        file_path = path.join(settings.MEDIA_ROOT, "clean_file.csv")

        if path.exists(file_path):
            try:
                with open(file_path, "rb") as fh:
                    file_content = fh.read()

                # Create an HTTP response with the file
                response = HttpResponse(file_content, content_type="text/csv")
                # Force download of file named "clean_file.csv"
                response["Content-Disposition"] = "attachment; filename=clean_file.csv"

                # os remove
                response.close = lambda: remove(file_path)

                return response
            except Exception as e:
                return HttpResponse(f"Error downloading file: {e}", status=500)
        else:
            return HttpResponse("The file does not exist.", status=404)

    def _prepare_context(self, df, name):
        columns = df.columns.tolist()
        values = df.values.tolist()
        counts = df.count().tolist()
        has_nulls = df.isnull().values.any()  # Bool

        print(f"nulls ?: {has_nulls}")

        # Pagination
        paginator = Paginator(values, 10)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        # Describe (General statistics)
        general_statistics = df.describe().to_dict()
        describe_info = self._extract_describe_info(general_statistics)

        data_frame_info = {key: count for key, count in zip(columns, counts)}

        data_frame_context = {
            "columns": columns,
            "values": values,
            "total_rows": data_frame_info,
        }

        chart_null = self._generate_heatmap(df)

        return {
            "form": UploadFileForm(),
            "name": name,
            "dataframe": data_frame_context,
            "page_obj": page_obj,
            "general_statistics": general_statistics.keys(),
            "describe_info": describe_info,
            "has_nulls": has_nulls,
            "chart_null": chart_null,
        }

    def _extract_describe_info(self, general_statistics):
        count = []
        mean = []
        std = []
        min_des = []
        percent_25 = []
        percent_50 = []
        percent_75 = []
        max_des = []

        for x in general_statistics.values():
            for k, v in x.items():
                if k == "count":
                    count.append(v)
                elif k == "mean":
                    mean.append(v)
                elif k == "std":
                    std.append(v)
                elif k == "min":
                    min_des.append(v)
                elif k == "25%":
                    percent_25.append(v)
                elif k == "50%":
                    percent_50.append(v)
                elif k == "75%":
                    percent_75.append(v)
                elif k == "max":
                    max_des.append(v)

        return {
            "count": count,
            "mean": mean,
            "std": std,
            "min": min_des,
            "25%": percent_25,
            "50%": percent_50,
            "75%": percent_75,
            "max": max_des,
        }

    def _generate_heatmap(self, df):
        plt.figure(figsize=(10, 6))
        sns.heatmap(df.isnull(), cbar=False, cmap="viridis", yticklabels=False)
        plt.title("Representation of Null values")

        # Save the graph to memory as an image
        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        plt.close()

        # Encode the image in base64
        image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        buffer.close()

        return image_base64
