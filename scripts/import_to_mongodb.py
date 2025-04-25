import os
import json
from pymongo import MongoClient

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/") 
db = client["sfs_infobot_db"]

# Get absolute base path of this script
base_path = os.path.dirname(os.path.abspath(__file__))

# Function to load and insert JSON files into MongoDB
def load_files_from_folder(folder_relative_path, collection_name):
    folder_path = os.path.join(base_path, folder_relative_path)
    collection = db[collection_name]

    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    if isinstance(data, list):
                        for item in data:
                            if isinstance(item, dict):
                                item['category'] = folder_relative_path
                                item['filename'] = filename
                                collection.insert_one(item)
                        print(f"Inserted list from {filename} into '{collection_name}'")
                    elif isinstance(data, dict):
                        data['category'] = folder_relative_path
                        data['filename'] = filename
                        collection.insert_one(data)
                        print(f"Inserted: {filename} into '{collection_name}'")
                    else:
                        print(f"Unsupported data format in {filename}")
                except json.JSONDecodeError as e:
                    print(f"Error decoding {filename}: {e}")


# Load all relevant folders
load_files_from_folder("courses/pg_courses", "courses")
load_files_from_folder("courses/ug_courses", "courses")
load_files_from_folder("compliance", "compliance")

