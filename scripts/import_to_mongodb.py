import os
import json
from pymongo import MongoClient

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["sfs_infobot_db"]

# Get absolute base path of the parent directory (project root)
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bot_data_path = os.path.join(base_path, "bot_data")

# Function to load and insert JSON files into MongoDB
def load_json_to_mongodb(folder_path, collection_name):
    collection = db[collection_name]
    if not os.path.exists(folder_path):
        print(f"Warning: {folder_path} does not exist. Skipping...")
        return
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

# Directories to process with their corresponding collection names
folder_collection_map = {
    "bot_data/Alumni_Achievements_Clubs": "alumni_achievements_clubs",
    "bot_data/College_News_ Events": "college_news_events",
    "bot_data/contact": "contact",
    "bot_data/courses/pg_courses": "pg_courses",
    "bot_data/courses/ug_courses": "ug_courses",
    "bot_data/events": "events",
    "bot_data/facilities": "facilities",
    "bot_data/institute_info": "institute_info",
    "bot_data/institute_info/admissions": "admissions",
    "bot_data/institute_info/placements": "placements",
    "bot_data/Results_and_exam": "results_and_exam",
    "bot_data/Skill_Development_Workshops": "skill_development_workshops"
}

# Load all folders into MongoDB
for relative_path, collection_name in folder_collection_map.items():
    abs_folder_path = os.path.join(base_path, relative_path)
    load_json_to_mongodb(abs_folder_path, collection_name)

# Close MongoDB connection
client.close()
print("All JSON files loaded into MongoDB.")
