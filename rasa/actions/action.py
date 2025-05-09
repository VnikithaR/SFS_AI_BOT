from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from pymongo import MongoClient
from rasa_sdk.events import SlotSet

# MongoDB connection details
MONGO_URI = "mongodb://localhost:27017"  # MongoDB URI
DB_NAME = "sfs_info_bot"  # Database name
COLLECTION_NAME = "user_data"  # Collection name

class ActionSaveUserName(Action):
    """
    This action saves the user's name to MongoDB after they log in.
    """
    def name(self) -> str:
        return "action_save_user_name"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        # Extract the user's name from the tracker (assuming the user provided it during login)
        user_name = tracker.get_slot("user_name")

        if user_name:
            # Connect to MongoDB
            client = MongoClient(MONGO_URI)
            db = client[DB_NAME]
            collection = db[COLLECTION_NAME]

            # Use the user's sender_id (unique ID) to store the data
            user_id = tracker.sender_id

            # Check if the user already exists in the database
            user = collection.find_one({"user_id": user_id})

            if user:
                # If the user exists, update their name (optional, if they change it)
                collection.update_one({"user_id": user_id}, {"$set": {"name": user_name}})
            else:
                # If the user doesn't exist, create a new record with their name
                collection.insert_one({"user_id": user_id, "name": user_name})

            # Inform the user that their name has been saved
            dispatcher.utter_message(f"Thank you, {user_name}, your name has been saved!")

        else:
            dispatcher.utter_message("Sorry, I couldn't retrieve your name. Please try again.")

        return []


class ActionFetchUserName(Action):
    """
    This action fetches the user's name from MongoDB and sends a personalized response.
    """
    def name(self) -> str:
        return "action_fetch_user_name"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        # Connect to MongoDB
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        # Use the sender_id to fetch the user data
        user_id = tracker.sender_id

        # Fetch user data based on the user_id
        user_data = collection.find_one({"user_id": user_id})

        if user_data:
            # Get the user's name from the database
            user_name = user_data.get("name", "User")
            dispatcher.utter_message(f"Hello {user_name}, how can I assist you today?")
        else:
            # If no user data exists, ask for the name
            dispatcher.utter_message("Hello! I don't have your name on file. Could you please tell me your name?")

        return []

