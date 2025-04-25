import json
import os
from typing import Any, Text, Dict, List
from pymongo import MongoClient
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# Initialize MongoDB client
client = MongoClient("mongodb://localhost:27017/")
db = client["sfs_infobot_db"]

# -----------------------------------------------------------------------------------
# PG Courses Available
# -----------------------------------------------------------------------------------
class ActionGetCourses(Action):
    def name(self) -> Text:
        return "action_get_courses"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Fetch the PG courses list from the database
        course_doc = db.courses.find_one({"category": "courses/pg_courses"})
        if not course_doc:
            dispatcher.utter_message(text="Sorry, I couldn't fetch the PG courses list right now.")
            return []

        course_list = course_doc.get("pg_courses", [])
        if not course_list:
            dispatcher.utter_message(text="No PG courses found in the database.")
            return []

        response = "📚 Available PG Courses:\n" + "\n".join(f"- {course}" for course in course_list)
        dispatcher.utter_message(text=response)
        return []

# -----------------------------------------------------------------------------------
# PG Fee Details
# -----------------------------------------------------------------------------------
class ActionFetchCourseFee(Action):
    def name(self) -> Text:
        return "action_fetch_course_fee"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        course_name = tracker.get_slot("course_name")
        fee_type = tracker.get_slot("fee_type") or ""

        if not course_name:
            dispatcher.utter_message(text="Please specify the course name to get fee details.")
            return []

        # Normalize course_name key for DB
        normalized_key = course_name.lower().replace(" ", "_").replace("(", "").replace(")", "").replace(".", "").replace("-", "_")
        course_doc = db.pg_courses_fee_details.find_one({"course_name": {"$regex": normalized_key, "$options": "i"}})

        if not course_doc:
            dispatcher.utter_message(text=f"Sorry, I couldn't find fee details for '{course_name}'.")
            return []

        course = course_doc
        annual_fee = course.get("annual_fee", {})
        semester_fee = course.get("mba_mgmt_semester_fee") or \
                       course.get("mba_pgcet_semester_fee") or \
                       course.get("mca_mgmt_semester_fee") or \
                       course.get("mca_pgcet_semester_fee") or \
                       course.get("mcom_fee_semester_fee") or \
                       course.get("msc_math_semester_fee") or \
                       course.get("semester_fee") or \
                       course.get("ma_eco_semester_fee")

        additional_fee = course.get("additional_fee", {})

        fee_details = f"💰 Fee Details for *{course['course_name']}*:\n"

        if "semester" in fee_type or "odd" in fee_type or "even" in fee_type:
            if semester_fee:
                if "odd" in fee_type:
                    odd = semester_fee.get("oddsem_fee", {})
                    fee_details += f"• Odd Semester Fee: {odd.get('total_fee', 'N/A')}\n"
                elif "even" in fee_type:
                    even = semester_fee.get("even_sem_fee", {})
                    fee_details += f"• Even Semester Fee: {even.get('total_fee', 'N/A')}\n"
                else:
                    odd = semester_fee.get("oddsem_fee", {})
                    even = semester_fee.get("even_sem_fee", {})
                    fee_details += f"• Odd Semester Fee: {odd.get('total_fee', 'N/A')}\n"
                    fee_details += f"• Even Semester Fee: {even.get('total_fee', 'N/A')}\n"
            else:
                fee_details += "Semester fee details not available.\n"

        elif "total" in fee_type or "grand" in fee_type:
            total = semester_fee.get("grand_total_fee") if semester_fee else "N/A"
            fee_details += f"• Grand Total Fee: {total}\n"

        else:  # Default to annual
            fee_details += f"• First Year Fee: {annual_fee.get('first_year_fee', 'N/A')}\n"
            fee_details += f"• Second Year Fee: {annual_fee.get('second_year_fee', 'N/A')}\n"

        if additional_fee:
            fee_details += f"• Uniform Fee: {additional_fee.get('uniform_fee', 'N/A')}\n"
            fee_details += f"• Non-Karnataka Fee: {additional_fee.get('non_karnataka_fee', 'N/A')}"

        dispatcher.utter_message(text=fee_details)
        return []

# -----------------------------------------------------------------------------------
# PG Syllabus
# -----------------------------------------------------------------------------------
class ActionFetchSyllabus(Action):
    def name(self) -> Text:
        return "action_fetch_syllabus"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        course_name = tracker.get_slot("course_name")
        if not course_name:
            dispatcher.utter_message(text="Please specify the course name to get the syllabus.")
            return []

        # Normalize the course_name to match JSON keys
        normalized_key = course_name.lower().replace(" ", "_").replace("(", "").replace(")", "").replace(".", "").replace("-", "_")

        # Path to syllabus JSON file
        file_path = "bot_data/courses/pg_courses/pg_syllabus.json"
        if not os.path.exists(file_path):
            dispatcher.utter_message(text="Syllabus data not found.")
            return []

        with open(file_path, "r") as f:
            syllabus_data = json.load(f)

        # Try to find matching key
        key = None
        for k, v in syllabus_data.items():
            if k.startswith(normalized_key):
                key = k
                break

        if not key:
            dispatcher.utter_message(text=f"Sorry, I couldn't find syllabus for '{course_name}'.")
            return []

        syllabus = syllabus_data[key]
        response = f"📄 Syllabus for *{course_name}*:\n"
        for year, link in syllabus.items():
            response += f"• {year.replace('_', ' ').title()}: {link}\n"

        dispatcher.utter_message(text=response)
        return []
