from django.core.paginator import Paginator
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

            # Details
            columns = df.columns.tolist()
            values = df.values.tolist()
            counts = df.count().tolist()
            has_nulls = df.isnull().values.any()  # Bool

            print(has_nulls)

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
                },
            )

        # To reload invalid form
        return render(request, "analytics/home.html", {"form": form})
