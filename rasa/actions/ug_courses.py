from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pymongo

# Replace with your MongoDB connection details
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "sfs_infobot_db"
COLLECTION_NAME = "ug_courses"  

class ActionListUGCourses(Action):
    def name(self) -> Text:
        return "action_list_ug_courses"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            client = pymongo.MongoClient(MONGO_URI)
            db = client[DATABASE_NAME]
            courses_data = db[COLLECTION_NAME].find_one({"ug_courses": {"$exists": True}})

            if courses_data and "ug_courses" in courses_data:
                ug_courses = ", ".join(courses_data["ug_courses"])
                dispatcher.utter_message(text=f"We offer the following undergraduate courses: {ug_courses}")
            else:
                dispatcher.utter_message(text="Sorry, I couldn't retrieve the list of courses at the moment.")

        except pymongo.errors.ConnectionFailure as e:
            print(f"Error connecting to MongoDB: {e}")
            dispatcher.utter_message(text="Sorry, I'm having trouble connecting to the database.")
        except Exception as e:
            print(f"Error fetching courses: {e}")
            dispatcher.utter_message(text="Sorry, there was an error retrieving the course list.")

        finally:
            if 'client' in locals() and client:
                client.close()

        return []

class ActionShowCourseDetails(Action):
    def name(self) -> Text:
        return "action_show_course_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        course_name = tracker.get_slot("course_name")

        if course_name:
            try:
                client = pymongo.MongoClient(MONGO_URI)
                db = client[DATABASE_NAME]
                departments_data = db[COLLECTION_NAME].find_one({"departments": {"$exists": True}})

                course_details = None
                if departments_data and "departments" in departments_data:
                    for dept in departments_data["departments"]:
                        for program in dept.get("programs", []):
                            if program.get("name", "").lower() == course_name.lower():
                                course_details = program
                                break
                        if course_details:
                            break

                if course_details:
                    details_text = f"Duration: {course_details.get('duration', 'Not specified')}\n"
                    if "specializations" in course_details:
                        details_text += f"Specializations: {', '.join(course_details['specializations'])}\n"
                    if "professional_certifications" in course_details:
                        details_text += f"Professional Certifications: {', '.join(course_details['professional_certifications'])}\n"
                    details_text += f"Description: {course_details.get('description', 'No description available')}"
                    dispatcher.utter_message(text=f"Here are some details about {course_name}: {details_text}")
                else:
                    dispatcher.utter_message(text=f"Sorry, I couldn't find details for the course: {course_name}")

            except pymongo.errors.ConnectionFailure as e:
                print(f"Error connecting to MongoDB: {e}")
                dispatcher.utter_message(text="Sorry, I'm having trouble connecting to the database.")
            except Exception as e:
                print(f"Error fetching course details: {e}")
                dispatcher.utter_message(text="Sorry, there was an error retrieving the course details.")

            finally:
                if 'client' in locals() and client:
                    client.close()
        else:
            dispatcher.utter_message(text="Please specify which course you'd like details for.")

        return []

class ActionShowCourseFee(Action):
    def name(self) -> Text:
        return "action_show_course_fee"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        course_name = tracker.get_slot("course_name")

        if course_name:
            try:
                client = pymongo.MongoClient(MONGO_URI)
                db = client[DATABASE_NAME]
                fee_data = db[COLLECTION_NAME].find_one({"undergraduate_fee_structure.courses.course_name": {"$regex": f"^{course_name}$", "$options": "i"}})

                if fee_data and "undergraduate_fee_structure" in fee_data and "courses" in fee_data["undergraduate_fee_structure"]:
                    for course in fee_data["undergraduate_fee_structure"]["courses"]:
                        if course["course_name"].lower() == course_name.lower():
                            fee_details = f"Year 1: ₹{course.get('year_1_fee', 'N/A')}, Year 2: ₹{course.get('year_2_fee', 'N/A')}, Year 3: ₹{course.get('year_3_fee', 'N/A')}"
                            dispatcher.utter_message(text=f"The fee details for {course_name} are: {fee_details}")
                            return []

                semester_fee_data_doc = db[COLLECTION_NAME].find_one({"semester_wise_fee_breakdown.1st_year.course_name": {"$regex": f"^{course_name}$", "$options": "i"}})
                if semester_fee_data_doc and "semester_wise_fee_breakdown" in semester_fee_data_doc and "1st_year" in semester_fee_data_doc["semester_wise_fee_breakdown"]:
                    for course in semester_fee_data_doc["semester_wise_fee_breakdown"]["1st_year"]:
                        if course["course_name"].lower() == course_name.lower():
                            fee_details = f"First Year - Odd Semester: ₹{course.get('odd_semester', {}).get('total_fee', 'N/A')}, Even Semester: ₹{course.get('even_semester', {}).get('total_fee', 'N/A')}, Grand Total: ₹{course.get('grand_total', 'N/A')}"
                            dispatcher.utter_message(text=f"The first year semester-wise fee breakdown for {course_name} is: {fee_details}")
                            return []

                dispatcher.utter_message(text=f"Fee details not found for {course_name}.")

            except pymongo.errors.ConnectionFailure as e:
                print(f"Error connecting to MongoDB: {e}")
                dispatcher.utter_message(text="Sorry, I'm having trouble connecting to the database.")
            except Exception as e:
                print(f"Error fetching fee details: {e}")
                dispatcher.utter_message(text="Sorry, there was an error retrieving the fee details.")

            finally:
                if 'client' in locals() and client:
                    client.close()
        else:
            dispatcher.utter_message(text="Please specify which course you'd like the fee details for.")

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
            "bcom(travel & tourism)": "bcom_faculty_list", # Assuming same faculty as regular B.Com
            "bsc(mec & cjp)": "bsc_faculty_list",
            "bsc(pcm)": "bsc_faculty_list"
        }

        if course_name:
            faculty_list_key = faculty_key_mapping.get(course_name.lower())
            if faculty_list_key:
                try:
                    client = pymongo.MongoClient(MONGO_URI)
                    db = client[DATABASE_NAME]
                    faculty_data = db[COLLECTION_NAME].find_one({faculty_list_key: {"$exists": True}})

                    if faculty_data and faculty_list_key in faculty_data:
                        faculty_info = [f"{f['name']} (Qualification: {f['qualification']})" for f in faculty_data[faculty_list_key]]
                        if faculty_info:
                            dispatcher.utter_message(text=f"The faculty members for {course_name} are: {', '.join(faculty_info)}")
                        else:
                            dispatcher.utter_message(text=f"No faculty information found for {course_name}.")
                    else:
                        dispatcher.utter_message(text=f"Sorry, I couldn't retrieve the faculty list for {course_name} at the moment.")

                except pymongo.errors.ConnectionFailure as e:
                    print(f"Error connecting to MongoDB: {e}")
                    dispatcher.utter_message(text="Sorry, I'm having trouble connecting to the database.")
                except Exception as e:
                    print(f"Error fetching faculty list: {e}")
                    dispatcher.utter_message(text="Sorry, there was an error retrieving the faculty list.")

                finally:
                    if 'client' in locals() and client:
                        client.close()
            else:
                dispatcher.utter_message(text=f"Sorry, I don't have faculty information for the course: {course_name}.")
        else:
            dispatcher.utter_message(text="Please specify which course you'd like to know the faculty for.")

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

        if course_name:
            syllabus_key = syllabus_key_mapping.get(course_name.lower())
            if syllabus_key:
                try:
                    client = pymongo.MongoClient(MONGO_URI)
                    db = client[DATABASE_NAME]
                    syllabus_data = db[COLLECTION_NAME].find_one({syllabus_key: {"$exists": True}})

                    if syllabus_data and syllabus_key in syllabus_data:
                        syllabus_info = syllabus_data[syllabus_key].get("syllabus")
                        if syllabus_info:
                            syllabus_links = []
                            if isinstance(syllabus_info, list):
                                for item in syllabus_info:
                                    link_text = item.get("year") or item.get("title") or "Syllabus Link"
                                    link_url = item.get("url")
                                    if link_url:
                                        syllabus_links.append(f"{link_text}: {link_url}")
                            elif isinstance(syllabus_info, dict):
                                for year, url in syllabus_info.items():
                                    if url:
                                        syllabus_links.append(f"{year.replace('_', ' ').title()}: {url}")

                            if syllabus_links:
                                dispatcher.utter_message(text=f"Here's the syllabus for {course_name}: {', '.join(syllabus_links)}")
                            else:
                                dispatcher.utter_message(text=f"Syllabus links not found for {course_name}.")
                        else:
                            dispatcher.utter_message(text=f"Syllabus information not available for {course_name}.")
                    else:
                        dispatcher.utter_message(text=f"Sorry, I couldn't retrieve the syllabus for {course_name} at the moment.")

                except pymongo.errors.ConnectionFailure as e:
                    print(f"Error connecting to MongoDB: {e}")
                    dispatcher.utter_message(text="Sorry, I'm having trouble connecting to the database.")
                except Exception as e:
                    print(f"Error fetching syllabus: {e}")
                    dispatcher.utter_message(text="Sorry, there was an error retrieving the syllabus.")

                finally:
                    if 'client' in locals() and client:
                        client.close()
            else:
                dispatcher.utter_message(text=f"Sorry, I don't have syllabus information for the course: {course_name}.")
        else:
            dispatcher.utter_message(text="Please specify which course you'd like the syllabus for.")

        return []

class ActionShowDepartmentPrograms(Action):
    def name(self) -> Text:
        return "action_show_department_programs"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        department_name = tracker.get_slot("department_name")

        if department_name:
            try:
                client = pymongo.MongoClient(MONGO_URI)
                db = client[DATABASE_NAME]
                departments_data = db[COLLECTION_NAME].find_one({"departments.name": {"$regex": f"^{department_name}$", "$options": "i"}})

                if departments_data and "departments" in departments_data:
                    for dept in departments_data["departments"]:
                        if dept.get("name", "").lower() == department_name.lower() and "programs" in dept:
                            program_names = [program["name"] for program in dept["programs"]]
                            if program_names:
                                dispatcher.utter_message(text=f"The {department_name} department offers the following programs: {', '.join(program_names)}")
                                return []
                            else:
                                dispatcher.utter_message(text=f"No programs found under the {department_name} department.")
                                return []
                    dispatcher.utter_message(text=f"Sorry, I couldn't find information for the {department_name} department.")
                else:
                    dispatcher.utter_message(text=f"Sorry, I couldn't find information for the {department_name} department.")

            except pymongo.errors.ConnectionFailure as e:
                print(f"Error connecting to MongoDB: {e}")
                dispatcher.utter_message(text="Sorry, I'm having trouble connecting to the database.")
            except Exception as e:
                print(f"Error fetching department programs: {e}")
                dispatcher.utter_message(text="Sorry, there was an error retrieving the department programs.")

            finally:
                if 'client' in locals() and client:
                    client.close()
        else:
            dispatcher.utter_message(text="Please specify which department you'd like to know the programs for.")

        return []