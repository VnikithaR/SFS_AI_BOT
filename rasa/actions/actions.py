from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from pymongo import MongoClient
from rasa_sdk.events import SlotSet
from typing import Any, Text, Dict, List

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

        return [SlotSet("user_name", user_name)]


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
class ActionAboutCollege(Action):
    def name(self) -> Text:
        return "action_about_college"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        message = ("SFS College is a reputed institution affiliated with Bangalore University, "
                   "offering quality education in science, commerce, and arts streams.")
        dispatcher.utter_message(text=message)
        return []

class ActionCollegeLocation(Action):
    def name(self) -> Text:
        return "action_college_location"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        message = "The college is located in Hebbagodi, Bengaluru, Karnataka – 560099."
        dispatcher.utter_message(text=message)
        return []

class ActionCollegeContact(Action):
    def name(self) -> Text:
        return "action_college_contact"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        message = ("You can contact the college at:\n"
                   "📞 Phone: +91-9876543210\n"
                   "📧 Email: info@sfscollege.edu.in")
        dispatcher.utter_message(text=message)
        return []

class ActionCoursesOffered(Action):
    def name(self) -> Text:
        return "action_courses_offered"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        message = ("SFS College offers the following programs:\n"
                   "🎓 Undergraduate Courses: BCA, BBA, BCom, BA\n"
                   "🎓 Postgraduate Courses: MCom, MSc (Psychology)")
        dispatcher.utter_message(text=message)
        return []

class ActionPrincipalInfo(Action):
    def name(self) -> Text:
        return "action_principal_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

       message = (
    "Principal's Message\n\n"
    "Welcome to St. Francis de Sales College, Electronics City, Bengaluru! Whether you are an incoming or prospective student, "
    "faculty or staff member, a current member of the college community, an alumnus, or a visitor, I am delighted to welcome you to our great institution.\n\n"
    "Begun in 2004, St. Francis de Sales College, popularly known as SFS College, was a novel and daring venture of the South-West India Province "
    "of the Missionaries of St. Francis de Sales. Many selfless and esteemed women and men have worked hard to make this college an institution of excellence and great repute. "
    "I feel very honored and glad to be part of this Desalite family.\n\n"
    "\"Everything by Love\" has been the trademark slogan of the Fransalian Missionaries for centuries. At SFS College, we want to ensure that we do everything by love, and all are served with utmost care.\n\n"
    "The three distinctive values that define our college are excellence, efficiency, and transformation. We have a dedicated staff, talented students, and a supportive community that make these values come alive every day. "
    "I am moved by the hard work and service-mindedness of my leadership team, both the teaching and non-teaching staff. There is a sense of community and a spirit of positivity among us. "
    "We don't compromise on excellence and efficiency, but we also make sure that everything that we do is effective and transformative.\n\n"
    "Our students are our real treasure. Their passion for learning and diligence in completing the tasks entrusted to them are inspiring. The diverse backgrounds they bring, the curious and ever wondering minds they display, "
    "and the variety of experiences and thoughts they share make SFS College a special place. Interacting and working with them is one of the privileges that I have in being the Principal of this college. "
    "It is a great honor to see and hear how they grow and mature over the years, and how God works with each one of them, shaping them into women and men who become a blessing to the world.\n\n"
    "Situated on a beautiful campus, SFS College is a welcome home to anyone in the pursuit of knowledge and transformation. A wide variety of disciplines and academic programs are offered, "
    "and the students are taught to integrate their personal lives, classroom learning, and life in the community. We insist on discipline but we encourage freedom with responsibility.\n\n"
    "I hope your visit to this website helps you to get to know us more. If you are a prospective student, I extend to you a very warm welcome to our campus. If you are a visitor or well-wisher, "
    "I invite you to partner with us in the mission of education.\n\n"
    "With Warm Wishes and God’s Blessings,\nRev. Dr. Binu Edathumparambil, MSFS\nPrincipal, St. Francis de Sales College"
)

        dispatcher.utter_message(text=message)
        return []