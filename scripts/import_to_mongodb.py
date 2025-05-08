import os
import json
from pymongo import MongoClient

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["sfs_infobot_db"]

# Get absolute base path of the parent directory (project root)
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bot_data_path = os.path.join(base_path, "bot_data")

# Function to load and insert a single JSON file into MongoDB, with collection name as folder/file path
def load_file_to_collection(file_path):
    # Get the relative path of the file inside the bot_data folder (without the base_path)
    relative_path = os.path.relpath(file_path, bot_data_path)
    
    # Replace directory separators with underscores to avoid conflicts with MongoDB collection names
    collection_name = relative_path.replace(os.path.sep, '_').replace(".json", "")
    
    collection = db[collection_name]
    
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            if isinstance(data, list):
                collection.insert_many(data)
                print(f"Inserted {len(data)} items from {relative_path} into '{collection_name}'")
            elif isinstance(data, dict):
                collection.insert_one(data)
                print(f"Inserted 1 item from {relative_path} into '{collection_name}'")
            else:
                print(f"Unsupported data format in {relative_path}")
        except json.JSONDecodeError as e:
            print(f"Error decoding {relative_path}: {e}")
        except Exception as e:
            print(f"Error inserting into '{collection_name}' from {relative_path}: {e}")

# Walk through all subdirectories and load each JSON file
def load_all_json_files(base_directory):
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                load_file_to_collection(file_path)

# Start loading all JSON files
load_all_json_files(bot_data_path)

# Close MongoDB connection
client.close()
print("All JSON files loaded into MongoDB.")
