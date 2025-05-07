from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pymongo

# Replace with your MongoDB connection details
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "sfs_infobot_db"
COLLECTION_NAME = "facilities"  

class ActionListAllFacilities(Action):
    def name(self) -> Text:
        return "action_list_all_facilities"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            client = pymongo.MongoClient(MONGO_URI)
            db = client[DATABASE_NAME]
            facilities_collection = db["facilities"]
            all_facilities = set()

            for facility_doc in facilities_collection.find():
                if "facilities_at_sfs_college" in facility_doc:
                    for category, facilities_list in facility_doc["facilities_at_sfs_college"].items():
                        if isinstance(facilities_list, list):
                            for facility in facilities_list:
                                all_facilities.add(facility)
                        elif isinstance(facilities_list, dict):
                            if isinstance(facilities_list.get("facilities"), list):
                                for facility in facilities_list["facilities"]:
                                    if isinstance(facility, dict) and "name" in facility:
                                        all_facilities.add(facility["name"])
                                    elif isinstance(facility, str):
                                        all_facilities.add(facility)
                            elif isinstance(facilities_list.get("cultural_activities"), list):
                                for facility in facilities_list["cultural_activities"]:
                                    if isinstance(facility, dict) and "name" in facility:
                                        all_facilities.add(facility["name"])
                                    elif isinstance(facility, str):
                                        all_facilities.add(facility)
                            elif isinstance(facilities_list.get("sports_activities"), list):
                                for facility in facilities_list["sports_activities"]:
                                    if isinstance(facility, dict) and "name" in facility:
                                        all_facilities.add(facility["name"])
                                    elif isinstance(facility, str):
                                        all_facilities.add(facility)
                            elif isinstance(facilities_list.get("gym_facilities"), list):
                                for facility in facilities_list["gym_facilities"]:
                                    if isinstance(facility, dict) and "name" in facility:
                                        all_facilities.add(facility["name"])
                                    elif isinstance(facility, str):
                                        all_facilities.add(facility)
                            elif isinstance(facilities_list.get("yoga_facilities"), list):
                                for facility in facilities_list["yoga_facilities"]:
                                    if isinstance(facility, dict) and "name" in facility:
                                        all_facilities.add(facility["name"])
                                    elif isinstance(facility, str):
                                        all_facilities.add(facility)
                        elif isinstance(facilities_list, str):
                            all_facilities.add(facilities_list)

            if all_facilities:
                dispatcher.utter_message(text="St. Francis de Sales College offers a wide range of facilities including: " + ", ".join(sorted(list(all_facilities))))
            else:
                dispatcher.utter_message(text="Sorry, I couldn't retrieve the list of facilities at the moment.")

        except pymongo.errors.ConnectionFailure as e:
            print(f"Error connecting to MongoDB: {e}")
            dispatcher.utter_message(text="Sorry, I'm having trouble connecting to the database.")
        except Exception as e:
            print(f"Error fetching facilities: {e}")
            dispatcher.utter_message(text="Sorry, there was an error retrieving the facilities.")

        finally:
            if 'client' in locals() and client:
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

        facility_type = facility_type.lower()
        facility_details = []

        try:
            client = pymongo.MongoClient(MONGO_URI)
            db = client[DATABASE_NAME]
            facilities_collection = db["facilities"]

            for facility_doc in facilities_collection.find():
                for category, data in facility_doc.items():
                    if isinstance(data, dict):
                        for sub_category, items in data.items():
                            if isinstance(items, list):
                                for item in items:
                                    if isinstance(item, dict):
                                        for key, value in item.items():
                                            if isinstance(value, str) and facility_type in value.lower():
                                                details = f"{key.capitalize()}: {value}"
                                                if details not in facility_details:
                                                    facility_details.append(details)
                                            elif key.lower() == "types" and isinstance(value, list) and facility_type in ", ".join(value).lower():
                                                details = f"{key.capitalize()}: {', '.join(value)}"
                                                if details not in facility_details:
                                                    facility_details.append(details)
                                            elif key.lower() == "description" and facility_type in value.lower():
                                                if value not in facility_details:
                                                    facility_details.append(value)
                                    elif isinstance(item, str) and facility_type in item.lower():
                                        if item not in facility_details:
                                            facility_details.append(item)
                            elif isinstance(items, str) and facility_type in items.lower():
                                if items not in facility_details:
                                    facility_details.append(items)
                    elif isinstance(data, list):
                        for item in data:
                            if isinstance(item, str) and facility_type in item.lower():
                                if item not in facility_details:
                                    facility_details.append(item)

            if facility_details:
                dispatcher.utter_message(text=f"Here's some information about the {facility_type} facilities at SFS College:\n" + "\n".join(facility_details))
            else:
                dispatcher.utter_message(text=f"Sorry, I don't have specific details about '{facility_type}' at the moment.")

        except pymongo.errors.ConnectionFailure as e:
            print(f"Error connecting to MongoDB: {e}")
            dispatcher.utter_message(text="Sorry, I'm having trouble connecting to the database.")
        except Exception as e:
            print(f"Error fetching details for {facility_type}: {e}")
            dispatcher.utter_message(text=f"Sorry, there was an error retrieving details for '{facility_type}'.")

        finally:
            if 'client' in locals() and client:
                client.close()

        return []