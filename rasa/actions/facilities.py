from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pymongo

# MongoDB connection details
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "sfs_infobot_db"

# Mapping facility types to actual collection names
FACILITY_COLLECTIONS = {
    "cultural": "facilities_cultural_sports_facilities",
    "sports": "facilities_cultural_sports_facilities",
    "facilities_at_sfs": "facilities_facilities_at_sfs",
    "ict": "facilities_ict_facilities",
    "library": "facilities_library_facilities",
    "physical": "facilities_physical_facilities",
    "welfare": "facilities_welfare_facilities",
    "wifi": "facilities_wifi_facilities"
}

def get_mongo_client():
    try:
        return pymongo.MongoClient(MONGO_URI)
    except pymongo.errors.ConnectionFailure as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

class ActionListAllFacilities(Action):
    def name(self) -> Text:
        return "action_list_all_facilities"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        client = get_mongo_client()
        if not client:
            dispatcher.utter_message(text="Sorry, I'm having trouble connecting to the database.")
            return []

        all_facilities = set()

        try:
            db = client[DATABASE_NAME]
            for coll in FACILITY_COLLECTIONS.values():
                try:
                    collection = db[coll]
                    documents = collection.find({})
                    for doc in documents:
                        for key, value in doc.items():
                            if isinstance(value, list):
                                for item in value:
                                    if isinstance(item, dict) and "name" in item:
                                        all_facilities.add(item["name"])
                                    elif isinstance(item, str):
                                        all_facilities.add(item)
                            elif isinstance(value, dict):
                                for sub_key, sub_value in value.items():
                                    if isinstance(sub_value, list):
                                        for item in sub_value:
                                            if isinstance(item, dict) and "name" in item:
                                                all_facilities.add(item["name"])
                                            elif isinstance(item, str):
                                                all_facilities.add(item)
                                    elif isinstance(sub_value, str):
                                        all_facilities.add(sub_value)
                            elif isinstance(value, str):
                                all_facilities.add(value)
                except Exception as e:
                    print(f"Error reading from {coll}: {e}")
                    continue

            if all_facilities:
                dispatcher.utter_message(
                    text="St. Francis de Sales College offers the following facilities:\n" +
                         ", ".join(sorted(all_facilities)))
            else:
                dispatcher.utter_message(text="Sorry, I couldn't retrieve the list of facilities.")
        finally:
            client.close()

        return []

class ActionShowSpecificFacility(Action):
    def name(self) -> Text:
        return "action_show_specific_facility"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        facility_type = tracker.get_slot("facility_type")
        if not facility_type:
            dispatcher.utter_message(text="Please specify which facility you are interested in.")
            return []

        facility_type_lower = facility_type.strip().lower()
        matched_collection = None
        for key in FACILITY_COLLECTIONS:
            if key in facility_type_lower:
                matched_collection = FACILITY_COLLECTIONS[key]
                break

        if not matched_collection:
            dispatcher.utter_message(text=f"Sorry, I couldn't find details related to '{facility_type}'.")
            return []

        client = get_mongo_client()
        if not client:
            dispatcher.utter_message(text="Sorry, I'm having trouble connecting to the database.")
            return []

        facility_details = []

        try:
            db = client[DATABASE_NAME]
            collection = db[matched_collection]
            documents = collection.find({})

            for doc in documents:
                for key, value in doc.items():
                    if isinstance(value, list):
                        for item in value:
                            if isinstance(item, dict):
                                for k, v in item.items():
                                    if isinstance(v, str) and facility_type_lower in v.lower():
                                        facility_details.append(f"{k.capitalize()}: {v}")
                            elif isinstance(item, str) and facility_type_lower in item.lower():
                                facility_details.append(item)
                    elif isinstance(value, dict):
                        for sub_key, sub_val in value.items():
                            if isinstance(sub_val, list):
                                for item in sub_val:
                                    if isinstance(item, dict):
                                        for k, v in item.items():
                                            if isinstance(v, str) and facility_type_lower in v.lower():
                                                facility_details.append(f"{k.capitalize()}: {v}")
                                    elif isinstance(item, str) and facility_type_lower in item.lower():
                                        facility_details.append(item)
                            elif isinstance(sub_val, str) and facility_type_lower in sub_val.lower():
                                facility_details.append(sub_val)
                    elif isinstance(value, str) and facility_type_lower in value.lower():
                        facility_details.append(value)

            if facility_details:
                dispatcher.utter_message(
                    text=f"Here's what I found about the {facility_type} facilities:\n" + "\n".join(facility_details))
            else:
                dispatcher.utter_message(text=f"No specific details found for '{facility_type}'.")
        except Exception as e:
            print(f"Error fetching facility details: {e}")
            dispatcher.utter_message(text="An error occurred while retrieving the information.")
        finally:
            client.close()

        return []
