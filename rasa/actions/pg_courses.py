from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pymongo

# Replace with your MongoDB connection details
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "sfs_info_bot"

class ActionListPGCourses(Action):
    def name(self) -> Text:
        return "action_list_pg_courses"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            client = pymongo.MongoClient(MONGO_URI)
            db = client[DATABASE_NAME]
            courses_collection = db["pg_courses_available"]
            courses_data = courses_collection.find_one()

            if courses_data and "pg_courses" in courses_data:
                pg_courses = ", ".join(courses_data["pg_courses"])
                dispatcher.utter_message(text=f"We offer the following postgraduate courses: {pg_courses}")
            else:
                dispatcher.utter_message(text="Sorry, I couldn't retrieve the list of postgraduate courses at the moment.")

        except pymongo.errors.ConnectionFailure as e:
            print(f"Error connecting to MongoDB: {e}")
            dispatcher.utter_message(text="Sorry, I'm having trouble connecting to the database.")
        except Exception as e:
            print(f"Error fetching PG courses: {e}")
            dispatcher.utter_message(text="Sorry, there was an error retrieving the postgraduate course list.")

        finally:
            if 'client' in locals() and client:
                client.close()

        return []

class ActionShowPGCourseDetails(Action):
    def name(self) -> Text:
        return "action_show_pg_course_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        course_name = tracker.get_slot("pg_course_name")

        if course_name:
            try:
                client = pymongo.MongoClient(MONGO_URI)
                db = client[DATABASE_NAME]
                fee_collection = db["pg_fee_details"]
                course_data = None
                fee_data = fee_collection.find_one({"postgraduate_fee_structure.courses.course_name": course_name})

                if fee_data and "postgraduate_fee_structure" in fee_data and "courses" in fee_data["postgraduate_fee_structure"]:
                    for course in fee_data["postgraduate_fee_structure"]["courses"]:
                        if course["course_name"].lower() == course_name.lower():
                            course_data = course
                            break

                if course_data:
                    details_text = f"Year 1 Fee: ₹{course_data.get('year_1_fee', 'N/A')}\n"
                    details_text += f"Year 2 Fee: ₹{course_data.get('year_2_fee', 'N/A')}"
                    dispatcher.utter_message(text=f"Details for {course_name}:\n{details_text}")
                else:
                    dispatcher.utter_message(text=f"Sorry, I couldn't find details for {course_name}.")

            except pymongo.errors.ConnectionFailure as e:
                print(f"Error connecting to MongoDB: {e}")
                dispatcher.utter_message(text="Sorry, I'm having trouble connecting to the database.")
            except Exception as e:
                print(f"Error fetching PG course details: {e}")
                dispatcher.utter_message(text="Sorry, there was an error retrieving the details for {course_name}.")

            finally:
                if 'client' in locals() and client:
                    client.close()
        else:
            dispatcher.utter_message(text="Please specify which postgraduate course you'd like details for.")

        return []

class ActionShowPGCourseFee(Action):
    def name(self) -> Text:
        return "action_show_pg_course_fee"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        course_name = tracker.get_slot("pg_course_name")

        if course_name:
            try:
                client = pymongo.MongoClient(MONGO_URI)
                db = client[DATABASE_NAME]
                fee_collection = db["pg_fee_details"]
                fee_data = fee_collection.find_one({"postgraduate_fee_structure.courses.course_name": course_name})

                if fee_data and "postgraduate_fee_structure" in fee_data and "courses" in fee_data["postgraduate_fee_structure"]:
                    for course in fee_data["postgraduate_fee_structure"]["courses"]:
                        if course["course_name"].lower() == course_name.lower():
                            fee_details = f"Year 1: ₹{course.get('year_1_fee', 'N/A')}, Year 2: ₹{course.get('year_2_fee', 'N/A')}"
                            dispatcher.utter_message(text=f"The fee details for {course_name} are: {fee_details}")
                            return []

                    semester_fee_data = fee_data.get("semester_wise_fee_breakdown", {}).get("1st_year", [])
                    for course in semester_fee_data:
                        if course["course_name"].lower() == course_name.lower():
                            fee_details = f"First Year - Odd Semester: ₹{course.get('odd_semester', {}).get('total_fee', 'N/A')}, Even Semester: ₹{course.get('even_semester', {}).get('total_fee', 'N/A')}, Grand Total: ₹{course.get('grand_total', 'N/A')}"
                            dispatcher.utter_message(text=f"The first year semester-wise fee breakdown for {course_name} is: {fee_details}")
                            return []

                    dispatcher.utter_message(text=f"Fee details not found for {course_name}.")
                else:
                    dispatcher.utter_message(text=f"Sorry, I couldn't retrieve the fee details for {course_name} at the moment.")

            except pymongo.errors.ConnectionFailure as e:
                print(f"Error connecting to MongoDB: {e}")
                dispatcher.utter_message(text="Sorry, I'm having trouble connecting to the database.")
            except Exception as e:
                print(f"Error fetching PG course fee: {e}")
                dispatcher.utter_message(text="Sorry, there was an error retrieving the fee details for {course_name}.")

            finally:
                if 'client' in locals() and client:
                    client.close()
        else:
            dispatcher.utter_message(text="Please specify which postgraduate course you'd like the fee details for.")

        return []

class ActionShowPGCourseSyllabus(Action):
    def name(self) -> Text:
        return "action_show_pg_course_syllabus"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        course_name = tracker.get_slot("pg_course_name")
        syllabus_key_mapping = {
            "m.a (economics)": "ma_economics_syllabus_details",
            "m.sc (psychology)": "msc_psychology_syllabus",
            "m.sc (mathematics)": "msc_math_syllabus",
            "m.com": "mcom_syllabus",
            "mba (mgmt)": "mba_mgmt_syllabus",
            "mba (pgcet)": "mba_pgcet_syllabus",
            "mca (mgmt)": "mca_mgmt_syllabus",
            "mca (pgcet)": "mca_pgcet_syllabus"
        }

        if course_name:
            syllabus_key = syllabus_key_mapping.get(course_name.lower())
            if syllabus_key:
                try:
                    client = pymongo.MongoClient(MONGO_URI)
                    db = client[DATABASE_NAME]
                    syllabus_collection = db["pg_syllabus"]
                    syllabus_data = syllabus_collection.find_one()

                    if syllabus_data and syllabus_key in syllabus_data:
                        syllabus_info = syllabus_data[syllabus_key]
                        syllabus_links = []
                        if isinstance(syllabus_info, dict):
                            for year, url in syllabus_info.items():
                                if url and url != "Not available":
                                    syllabus_links.append(f"{year.replace('_', ' ').title()}: {url}")
                        elif isinstance(syllabus_info, str) and syllabus_info != "Not available":
                            syllabus_links.append(syllabus_info)

                        if syllabus_links:
                            dispatcher.utter_message(text=f"Here's the syllabus for {course_name}: {', '.join(syllabus_links)}")
                        else:
                            dispatcher.utter_message(text=f"Syllabus not available for {course_name} at the moment.")
                    else:
                        dispatcher.utter_message(text=f"Sorry, I couldn't retrieve the syllabus for {course_name}.")

                except pymongo.errors.ConnectionFailure as e:
                    print(f"Error connecting to MongoDB: {e}")
                    dispatcher.utter_message(text="Sorry, I'm having trouble connecting to the database.")
                except Exception as e:
                    print(f"Error fetching PG syllabus: {e}")
                    dispatcher.utter_message(text="Sorry, there was an error retrieving the syllabus for {course_name}.")

                finally:
                    if 'client' in locals() and client:
                        client.close()
            else:
                dispatcher.utter_message(text=f"Sorry, I don't have syllabus information for the course: {course_name}.")
        else:
            dispatcher.utter_message(text="Please specify which postgraduate course you'd like the syllabus for.")

        return []