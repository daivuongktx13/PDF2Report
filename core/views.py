from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
import pandas as pd
import glob
import os
import time

# Create your views here.

def index(request):
    template = loader.get_template("core/index.html")
    return HttpResponse(template.render({}, request))

@csrf_exempt
def convert_file(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        # Perform file conversion here
        file_path = os.path.join('static', uploaded_file.name)  # Replace with the desired file path
        
        # Save the file to the specified location
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        start = time.time()
        print("Execute command...")
        # os.system(f"python main.py --dir {file_path}")
        print("Execute command complete")
        folder = uploaded_file.name.split(".")[0]
        # os.system(f"cp -r ./result/{folder} ./static/")
        print(f"Time: {time.time() - start}")
        # Return a JSON response indicating success
        return JsonResponse({'url': f'/view?run={folder}'})
    else:
        # Return a JSON response indicating failure
        return JsonResponse({'url': 'Not any File'})
    

def view(request):
    run_name = request.GET.get('run')
    template = loader.get_template("core/view.html")
    csv_file_paths = glob.glob(f"static/{run_name}/balance/image*.csv")
    imagefile_paths = glob.glob(f"static/{run_name}/balance/image*.jpg")
    tables = []
    for csv_file_path, image_file_path in zip(csv_file_paths, imagefile_paths):
        data = pd.read_csv(csv_file_path)
        data = data.fillna("")
        serialized_data = data.drop("Unnamed: 0", axis = 1).values
        table = {
            "image": "/".join(image_file_path.split("/")[1:]),
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