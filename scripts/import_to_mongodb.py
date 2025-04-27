import os
import json
from pymongo import MongoClient

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["sfs_info_bot"]

# Get absolute base path of the parent directory (project root)
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bot_data_path = os.path.join(base_path, "bot_data")
courses_path = os.path.join(bot_data_path, "courses")
pg_courses_path = os.path.join(courses_path, "pg_courses")
ug_courses_path = os.path.join(courses_path, "ug_courses")
events_path = os.path.join(bot_data_path, "events")
facilities_path = os.path.join(bot_data_path, "facilities")
institute_info_path = os.path.join(bot_data_path, "institute_info")
admissions_path = os.path.join(institute_info_path, "admissions")
placements_path = os.path.join(institute_info_path, "placemets") # Corrected typo

# Function to load and insert JSON files into MongoDB
def load_json_to_mongodb(folder_path, collection_name):
    collection = db[collection_name]
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    if isinstance(data, list):
                        collection.insert_many(data)
                        print(f"Inserted {len(data)} items from {filename} into '{collection_name}'")
                    elif isinstance(data, dict):
                        collection.insert_one(data)
                        print(f"Inserted 1 item from {filename} into '{collection_name}'")
                    else:
                        print(f"Unsupported data format in {filename}")
                except json.JSONDecodeError as e:
                    print(f"Error decoding {filename}: {e}")
                except Exception as e:
                    print(f"Error inserting into '{collection_name}' from {filename}: {e}")

# Load courses data
load_json_to_mongodb(pg_courses_path, "pg_courses")
load_json_to_mongodb(ug_courses_path, "ug_courses")

# Load events data
load_json_to_mongodb(events_path, "events")

# Load facilities data
load_json_to_mongodb(facilities_path, "facilities")

# Load institute info data
load_json_to_mongodb(institute_info_path, "institute_info")
load_json_to_mongodb(admissions_path, "admissions")
load_json_to_mongodb(placements_path, "placements") # Using corrected path

client.close()
print("All JSON files loaded into MongoDB.")