from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import pandas as pd
import glob
import os

# Create your views here.

def index(request):
    template = loader.get_template("core/index.html")
    return HttpResponse(template.render({}, request))

def view(request):
    template = loader.get_template("core/view.html")
    csv_file_paths = glob.glob("static/fpt/balance/image*.csv")
    tables = []
    for csv_file_path in csv_file_paths:
        data = pd.read_csv(csv_file_path)
        data = data.fillna("")
        serialized_data = data.drop("Unnamed: 0", axis = 1).values
        table = {
            "file_name": os.path.basename(csv_file_path),
            "table_titles" : serialized_data[0],
            "table_contents":  serialized_data[1:],
        }
        tables.append(table)
    context = {
        "tables": list(enumerate(tables)),
        "indexes": list(range(len(tables)))
    }
    return HttpResponse(template.render(context, request))