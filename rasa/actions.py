from typing import Any, Text, Dict, List
from pymongo import MongoClient
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# MongoDB client setup
client = MongoClient("mongodb://localhost:27017/")
db = client["sfs_infobot_db"]

class ActionGetCourses(Action):
    def name(self) -> Text:
        return "action_get_courses"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get the course_type slot value
        course_type = tracker.get_slot("course_type")

        # Query MongoDB based on course_type
        if course_type == "ug":
            courses_cursor = db.courses.find({"category": "courses/ug_courses"})
        elif course_type == "pg":
            courses_cursor = db.courses.find({"category": "courses/pg_courses"})
        else:
            courses_cursor = db.courses.find()  # Default to all courses if no specific type

        # Convert cursor to list to iterate
        courses = list(courses_cursor)

        if not courses:
            response = "Sorry, I couldn't find any courses matching that category."
        else:
            response = "Here are the courses:\n"
            for course in courses:
                course_name = course.get('name', 'Unnamed')  # Default to 'Unnamed' if no name
                response += f"- {course_name}\n"

        # Send response back to the user
        dispatcher.utter_message(text=response)

        return []
