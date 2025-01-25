from django.core.paginator import Paginator
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views import View
from .forms import UploadFileForm

# Others -> Graphs
import base64
from io import BytesIO

# Pandas
import pandas as pd

# To work with files directly with json
from io import StringIO

# Seaborn
import matplotlib

matplotlib.use("Agg")

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

            # Details
            columns = df.columns.tolist()
            values = df.values.tolist()
            counts = df.count().tolist()
            has_nulls = df.isnull().values.any()  # Bool

            print(f"nulls ?: {has_nulls}")

            # Pagination
            paginator = Paginator(values, 10)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)

            # Describe (General statistics)
            general_statistics = df.describe().to_dict()

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

            describe_info = {
                "count": count,
                "mean": mean,
                "std": std,
                "min": min_des,
                "25%": percent_25,
                "50%": percent_50,
                "75%": percent_75,
                "max": max_des,
            }

            data_frame_info = {key: count for key, count in zip(columns, counts)}

            data_frame_context = {
                "columns": columns,
                "values": values,
                "total_rows": data_frame_info,
            }

            # Graphs
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

            # "form": form -> To load valid form after submitting it
            return render(
                request,
                "analytics/home.html",
                {
                    "form": UploadFileForm(),
                    "name": name,
                    "dataframe": data_frame_context,
                    "page_obj": page_obj,
                    "general_statistics": general_statistics.keys(),
                    "describe_info": describe_info,
                    "has_nulls": has_nulls,
                    "chart_null": image_base64,
                },
            )
        else:
            return render(request, "analytics/home.html", {"form": UploadFileForm()})

    def post(self, request):
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

            # Isnull
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

            # Save the dataframe in SESSIONS
            request.session["name"] = name
            request.session["dataframe"] = df.to_json()

            # Details
            columns = df.columns.tolist()
            values = df.values.tolist()
            counts = df.count().tolist()
            has_nulls = df.isnull().values.any()  # Bool

            print(f"nulls ?: {has_nulls}")

            # Pagination
            paginator = Paginator(values, 10)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)

            # Describe (General statistics)
            general_statistics = df.describe().to_dict()

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

            describe_info = {
                "count": count,
                "mean": mean,
                "std": std,
                "min": min_des,
                "25%": percent_25,
                "50%": percent_50,
                "75%": percent_75,
                "max": max_des,
            }

            data_frame_info = {key: count for key, count in zip(columns, counts)}

            data_frame_context = {
                "columns": columns,
                "values": values,
                "total_rows": data_frame_info,
            }

            # Graphs
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

            # "form": form -> To load valid form after submitting it
            return render(
                request,
                "analytics/home.html",
                {
                    "form": form,
                    "name": name,
                    "dataframe": data_frame_context,
                    "page_obj": page_obj,
                    "general_statistics": general_statistics.keys(),
                    "describe_info": describe_info,
                    "has_nulls": has_nulls,
                    "chart_null": image_base64,
                },
            )

        # To reload invalid form
        return render(request, "analytics/home.html", {"form": form})
