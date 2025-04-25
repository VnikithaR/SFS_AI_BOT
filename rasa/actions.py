import json
import os
from typing import Any, Text, Dict, List
from pymongo import MongoClient
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# Initialize MongoDB client
client = MongoClient("mongodb://localhost:27017/")
db = client["sfs_infobot_db"]

class ActionGetCourses(Action):
    def name(self) -> Text:
        return "action_get_courses"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

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
        key = next((k for k in db.pg_courses_fee_details.keys() if db.pg_courses_fee_details[k]["course_name"].lower() == course_name.lower()), None)

        if not key:
            dispatcher.utter_message(text=f"Sorry, I couldn't find fee details for '{course_name}'.")
            return []

        course = db.pg_courses_fee_details[key]
        annual_fee = course.get("annual_fee", {})
        additional_fee = course.get("mba_mgmt_additional_fee") or \
                         course.get("mba_pgcet_additional_fee") or \
                         course.get("mca_mgmt_additional_fee") or \
                         course.get("mca_pgcet_additional_fee") or \
                         course.get("mcom_fee_additional_fee") or \
                         course.get("msc_math_additional_fee") or \
                         course.get("msc_math_additional_fee") or \
                         course.get("ma_eco_additional_fee")

        semester_fee = course.get("mba_mgmt_semester_fee") or \
                       course.get("mba_pgcet_semester_fee") or \
                       course.get("mca_mgmt_semester_fee") or \
                       course.get("mca_pgcet_semester_fee") or \
                       course.get("mcom_fee_semester_fee") or \
                       course.get("msc_math_semester_fee") or \
                       course.get("semester_fee") or \
                       course.get("ma_eco_semester_fee")

        # Build response based on fee_type
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
class ActionFetchNaacInfo(Action):
    def name(self) -> Text:
        return "action_fetch_naac_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        compliance_doc = db.compliance.find_one({"filename": "naac_data.json"})
        if not compliance_doc:
            dispatcher.utter_message(text="NAAC accreditation information is currently unavailable.")
            return []

        message = compliance_doc.get("message", "NAAC information not found.")
        dispatcher.utter_message(text=message)
        return []

class ActionGetBBA(Action):
    def name(self) -> str:
        return "action_get_bba_syllabus"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text="Please choose one of the following options for the BBA syllabus: \n1. BBA Regular \n2. BBA Aviation")
        return []


class ActionGetBBARegular(Action):
    def name(self) -> str:
        return "action_get_bba_regular_syllabus"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        course_doc = db.BBA_Regular_syllabus.find_one()
        if not course_doc:
            dispatcher.utter_message(text="Sorry, I couldn't fetch the BBA Regular syllabus.")
            return []
        
        syllabus_details = course_doc.get("syllabus", [])
        response = "📚 BBA Regular Syllabus:\n"
        for item in syllabus_details:
            response += f"- {item['year']}: {item['url']}\n"
        
        dispatcher.utter_message(text=response)
        return []


class ActionGetBBAAviation(Action):
    def name(self) -> str:
        return "action_get_bba_aviation_syllabus"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        course_doc = db.BBA_Aviation_syllabus.find_one()
        if not course_doc:
            dispatcher.utter_message(text="Sorry, I couldn't fetch the BBA Aviation syllabus.")
            return []
        
        syllabus_details = course_doc.get("syllabus", [])
        response = "📚 BBA Aviation Syllabus:\n"
        for item in syllabus_details:
            response += f"- {item['year']}: {item['url']}\n"
        
        dispatcher.utter_message(text=response)
        return []


class ActionGetBSC(Action):
    def name(self) -> str:
        return "action_get_bsc_syllabus"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text="Please choose one of the following options for the BSC syllabus: \n1. BSC MEC \n2. BSC PCM")
        return []


class ActionGetBSCChemistry(Action):
    def name(self) -> str:
        return "action_get_bsc_mec_syllabus"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        course_doc = db.BSC_MEC_CJP_syllabus.find_one()
        if not course_doc:
            dispatcher.utter_message(text="Sorry, I couldn't fetch the BSC MEC syllabus.")
            return []
        
        syllabus_details = course_doc.get("syllabus", [])
        response = "📚 BSC MEC Syllabus:\n"
        for item in syllabus_details:
            response += f"- {item['year']}: {item['url']}\n"
        
        dispatcher.utter_message(text=response)
        return []


class ActionGetBSCPCM(Action):
    def name(self) -> str:
        return "action_get_bsc_pcm_syllabus"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        course_doc = db.BSC_PCM_syllabus.find_one()
        if not course_doc:
            dispatcher.utter_message(text="Sorry, I couldn't fetch the BSC PCM syllabus.")
            return []
        
        syllabus_details = course_doc.get("syllabus", [])
        response = "📚 BSC PCM Syllabus:\n"
        for item in syllabus_details:
            response += f"- {item['year']}: {item['url']}\n"
        
        dispatcher.utter_message(text=response)
        return []


class ActionGetBCom(Action):
    def name(self) -> str:
        return "action_get_bcom_syllabus"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text="Please choose one of the following options for the BCom syllabus: \n1. BCom Regular \n2. BCom Travel & Tourism")
        return []


class ActionGetBComRegular(Action):
    def name(self) -> str:
        return "action_get_bcom_regular_syllabus"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        course_doc = db.BCOM_Regular_syllabus.find_one()
        if not course_doc:
            dispatcher.utter_message(text="Sorry, I couldn't fetch the BCom Regular syllabus.")
            return []
        
        syllabus_details = course_doc.get("syllabus", [])
        response = "📚 BCom Regular Syllabus:\n"
        for item in syllabus_details:
            response += f"- {item['year']}: {item['url']}\n"
        
        dispatcher.utter_message(text=response)
        return []


class ActionGetBComTravelTourism(Action):
    def name(self) -> str:
        return "action_get_bcom_travel_tourism_syllabus"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        course_doc = db.BCOM_Travel_Tourism_syllabus.find_one()
        if not course_doc:
            dispatcher.utter_message(text="Sorry, I couldn't fetch the BCom Travel & Tourism syllabus.")
            return []
        
        syllabus_details = course_doc.get("syllabus", [])
        response = "📚 BCom Travel & Tourism Syllabus:\n"
        for item in syllabus_details:
            response += f"- {item['year']}: {item['url']}\n"
        
        dispatcher.utter_message(text=response)
        return []