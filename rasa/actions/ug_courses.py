from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pymongo

# MongoDB connection details
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "sfs_infobot_db"

UG_COURSES_COLLECTION = "courses_ug_courses_ug_courses_available"
UG_FACULTY_COLLECTION = "courses_ug_courses_ug_faculties"
UG_FEE_COLLECTION = "courses_ug_courses_ug_fee_details"
UG_PROGRAMS_COLLECTION = "courses_ug_courses_ug_programs_details"
UG_SYLLABUS_COLLECTION = "courses_ug_courses_ug_syllabus"

def get_mongo_client():
    try:
        return pymongo.MongoClient(MONGO_URI)
    except pymongo.errors.ConnectionFailure as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

class ActionListUGCourses(Action):
    def name(self) -> Text:
        return "action_list_ug_courses"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        client = get_mongo_client()
        if client is None:
            dispatcher.utter_message(text="Sorry, I'm having trouble connecting to the database.")
            return []

        try:
            db = client[DATABASE_NAME]
            data = db[UG_COURSES_COLLECTION].find_one()

            if data and "ug_courses" in data:
                courses = ", ".join(data["ug_courses"])
                dispatcher.utter_message(text=f"We offer the following undergraduate courses: {courses}")
            else:
                dispatcher.utter_message(text="Sorry, I couldn't retrieve the list of courses at the moment.")
        except Exception as e:
            print(f"Error fetching courses: {e}")
            dispatcher.utter_message(text="Sorry, there was an error retrieving the course list.")
        finally:
            client.close()

        return []

class ActionShowCourseDetails(Action):
    def name(self) -> Text:
        return "action_show_course_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        course_name = tracker.get_slot("course_name")
        if not course_name:
            dispatcher.utter_message(text="Please specify which course you'd like details for.")
            return []

        client = get_mongo_client()
        if client is None:
            dispatcher.utter_message(text="Sorry, I'm having trouble connecting to the database.")
            return []

        try:
            db = client[DATABASE_NAME]
            data = db[UG_PROGRAMS_COLLECTION].find_one()

            if not data or "departments" not in data:
                dispatcher.utter_message(text="No program details found.")
                return []

            for dept in data["departments"]:
                for prog in dept.get("programs", []):
                    if prog.get("name", "").lower() == course_name.lower():
                        text = f"Duration: {prog.get('duration', 'Not specified')}\n"
                        if "specializations" in prog:
                            text += f"Specializations: {', '.join(prog['specializations'])}\n"
                        if "professional_certifications" in prog:
                            text += f"Certifications: {', '.join(prog['professional_certifications'])}\n"
                        text += f"Description: {prog.get('description', 'No description available')}"
                        dispatcher.utter_message(text=f"Here are some details about {course_name}:\n{text}")
                        return []
            dispatcher.utter_message(text=f"Sorry, I couldn't find details for the course: {course_name}")
        except Exception as e:
            print(f"Error fetching course details: {e}")
            dispatcher.utter_message(text="Sorry, there was an error retrieving the course details.")
        finally:
            client.close()

        return []

class ActionShowCourseFee(Action):
    def name(self) -> Text:
        return "action_show_course_fee"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        course_name = tracker.get_slot("course_name")
        if not course_name:
            dispatcher.utter_message(text="Please specify which course you'd like the fee details for.")
            return []

        client = get_mongo_client()
        if client is None:
            dispatcher.utter_message(text="Sorry, I'm having trouble connecting to the database.")
            return []

        try:
            db = client[DATABASE_NAME]
            fee_data = db[UG_FEE_COLLECTION].find_one({"undergraduate_fee_structure.courses.course_name": {"$regex": f"^{course_name}$", "$options": "i"}})

            if fee_data:
                for course in fee_data.get("undergraduate_fee_structure", {}).get("courses", []):
                    if course["course_name"].lower() == course_name.lower():
                        fee_text = f"Year 1: ₹{course.get('year_1_fee', 'N/A')}, Year 2: ₹{course.get('year_2_fee', 'N/A')}, Year 3: ₹{course.get('year_3_fee', 'N/A')}"
                        dispatcher.utter_message(text=f"The fee details for {course_name} are: {fee_text}")
                        return []

                sem_data = fee_data.get("semester_wise_fee_breakdown", {}).get("1st_year", [])
                for course in sem_data:
                    if course["course_name"].lower() == course_name.lower():
                        sem_text = f"Odd Sem: ₹{course['odd_semester']['total_fee']}, Even Sem: ₹{course['even_semester']['total_fee']}, Total: ₹{course['grand_total']}"
                        dispatcher.utter_message(text=f"The semester-wise fee for {course_name} is: {sem_text}")
                        return []

            dispatcher.utter_message(text=f"Fee details not found for {course_name}.")
        except Exception as e:
            print(f"Error fetching fee details: {e}")
            dispatcher.utter_message(text="Sorry, there was an error retrieving the fee details.")
        finally:
            client.close()

        return []

class ActionShowCourseFaculty(Action):
    def name(self) -> Text:
        return "action_show_course_faculty"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        course_name = tracker.get_slot("course_name")
        faculty_key_mapping = {
            "ba(hep & hes)": "ba_faculty_list",
            "ba(jpe & sep)": "ba_faculty_list",
            "bba(aviation)": "bba_aviation_faculty_list",
            "bba(regular)": "bba_reg_faculty_list",
            "bca": "bca_faculty_list",
            "bcom(regular)": "bcom_faculty_list",
            "bcom(travel & tourism)": "bcom_faculty_list",
            "bsc(mec & cjp)": "bsc_faculty_list",
            "bsc(pcm)": "bsc_faculty_list"
        }

        faculty_key = faculty_key_mapping.get(course_name.lower())
        if not faculty_key:
            dispatcher.utter_message(text=f"Sorry, I don't have faculty information for {course_name}.")
            return []

        client = get_mongo_client()
        if client is None:
            dispatcher.utter_message(text="Sorry, I'm having trouble connecting to the database.")
            return []

        try:
            db = client[DATABASE_NAME]
            data = db[UG_FACULTY_COLLECTION].find_one({faculty_key: {"$exists": True}})

            if data and faculty_key in data:
                faculty = data[faculty_key]
                faculty_list = [f"{f['name']} (Qualification: {f['qualification']})" for f in faculty]
                dispatcher.utter_message(text=f"The faculty members for {course_name} are: {', '.join(faculty_list)}")
            else:
                dispatcher.utter_message(text=f"Sorry, no faculty information found for {course_name}.")
        except Exception as e:
            print(f"Error fetching faculty list: {e}")
            dispatcher.utter_message(text="Sorry, there was an error retrieving the faculty list.")
        finally:
            client.close()

        return []

class ActionShowCourseSyllabus(Action):
    def name(self) -> Text:
        return "action_show_course_syllabus"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        course_name = tracker.get_slot("course_name")
        syllabus_key_mapping = {
            "ba(hep & hes)": "BA_HEP_HES_syllabus",
            "ba(jpe & sep)": "BA_JPE_SEP_syllabus",
            "bba(aviation)": "BBA_Aviation_syllabus",
            "bba(regular)": "BBA_Regular_syllabus",
            "bca": "BCA_syllabus",
            "bcom(regular)": "BCOM_Regular_syllabus",
            "bcom(travel & tourism)": "BCOM_Travel_Tourism_syllabus",
            "bsc(mec & cjp)": "BSC_MEC_CJP_syllabus",
            "bsc(pcm)": "BSC_PCM_syllabus"
        }

        syllabus_key = syllabus_key_mapping.get(course_name.lower())
        if not syllabus_key:
            dispatcher.utter_message(text=f"Sorry, I don't have syllabus information for {course_name}.")
            return []

        client = get_mongo_client()
        if client is None:
            dispatcher.utter_message(text="Sorry, I'm having trouble connecting to the database.")
            return []

        try:
            db = client[DATABASE_NAME]
            data = db[UG_SYLLABUS_COLLECTION].find_one({syllabus_key: {"$exists": True}})

            if data and syllabus_key in data:
                syllabus_data = data[syllabus_key].get("syllabus")
                links = []
                if isinstance(syllabus_data, list):
                    for entry in syllabus_data:
                        links.append(f"{entry.get('year', 'Year')}: {entry.get('url')}")
                elif isinstance(syllabus_data, dict):
                    links.append(f"{syllabus_data.get('title', 'Syllabus')}: {syllabus_data.get('url')}")
                dispatcher.utter_message(text=f"The syllabus for {course_name}:\n" + "\n".join(links))
            else:
                dispatcher.utter_message(text=f"No syllabus information found for {course_name}.")
        except Exception as e:
            print(f"Error fetching syllabus: {e}")
            dispatcher.utter_message(text="Sorry, there was an error retrieving the syllabus.")
        finally:
            client.close()

        return []
