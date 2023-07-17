import glob
import os
import pandas as pd

def getReportCategory(run_name, category):
    assert category in ["balance", "cashflow", "income"]
    csv_file_paths = glob.glob(f"static/{run_name}/{category}/image*.xlsx")
    imagefile_paths = glob.glob(f"static/{run_name}/{category}/image*.jpg")
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
    return {
        "tables": list(enumerate(tables)),
        "indexes": list(range(len(tables))),
        "name": category
    }

def getTextCategory(run_name):
    category = "financial_statement"
    text_file_paths = glob.glob(f"static/{run_name}/{category}/image*.txt")
    imagefile_paths = glob.glob(f"static/{run_name}/{category}/image*.jpg")
    texts = []
    for text_file_path, image_file_path in zip(text_file_paths, imagefile_paths):
        with open(text_file_path, 'r', encoding="utf-8") as file:
            content = file.read()
        text = {
            "image": "/".join(image_file_path.split("/")[1:]),
            "file_name": os.path.basename(text_file_path),
            "content": content
        }
        texts.append(text)
    return {
        "texts": list(enumerate(texts)),
        "indexes": list(range(len(texts))),
        "name": category
    }