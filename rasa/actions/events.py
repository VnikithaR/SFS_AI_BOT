from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pymongo
import datetime

# Replace with your MongoDB connection details
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "sfs_infobot_db"
COLLECTION_NAME = "ug_courses"  

def format_date(date_str):
    try:
        date_obj = datetime.datetime.strptime(date_str, "%d-%m-%Y")
        return date_obj.strftime("%B %d, %Y")
    except ValueError:
        try:
            date_obj = datetime.datetime.strptime(date_str, "%d-%b-%y")
            return date_obj.strftime("%B %d, %Y")
        except ValueError:
            return date_str

class ActionListCollegeEvents(Action):
    def name(self) -> Text:
        return "action_list_college_events"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            client = pymongo.MongoClient(MONGO_URI)
            db = client[DATABASE_NAME]
            events_collection = db["upcoming_events"]
            events_data = events_collection.find_one()

            if events_data and "upcoming_events" in events_data:
                events_list = []
                for event in events_data["upcoming_events"]:
                    date_str = format_date(event.get("date", "N/A"))
                    ug1 = event.get("ug1_event", "N/A")
                    ug2_3 = event.get("ug2_3_event", "N/A")
                    event_info = f"{date_str} ({event.get('day', 'N/A')}): "
                    if ug1 and ug2_3:
                        event_info += f"UG 1 - {ug1}; UG 2/3 - {ug2_3}"
                    elif ug1:
                        event_info += f"UG 1 - {ug1}"
                    elif ug2_3:
                        event_info += f"UG 2/3 - {ug2_3}"
                    else:
                        event_info += "No specific event mentioned"
                    events_list.append(event_info)

                if events_list:
                    dispatcher.utter_message(text="Here are the upcoming college events:\n" + "\n".join(events_list))
                else:
                    dispatcher.utter_message(text="There are no specific upcoming college events listed at the moment.")
            else:
                dispatcher.utter_message(text="Sorry, I couldn't retrieve the upcoming college events right now.")

        except pymongo.errors.ConnectionFailure as e:
            print(f"Error connecting to MongoDB: {e}")
            dispatcher.utter_message(text="Sorry, I'm having trouble connecting to the database.")
        except Exception as e:
            print(f"Error fetching upcoming events: {e}")
            dispatcher.utter_message(text="Sorry, there was an error retrieving the upcoming college events.")

        finally:
            if 'client' in locals() and client:
                client.close()

        return []

class ActionShowEventOnDate(Action):
    def name(self) -> Text:
        return "action_show_event_on_date"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        date_str = tracker.get_slot("date")
        if date_str:
            try:
                target_date = None
                try:
                    target_date = datetime.datetime.strptime(date_str, "%d-%m-%Y").strftime("%d-%m-%Y")
                except ValueError:
                    try:
                        target_date = datetime.datetime.strptime(date_str, "%d %B").strftime("%d-%m-%Y")
                    except ValueError:
                        try:
                            target_date = datetime.datetime.strptime(date_str, "%B %d, %Y").strftime("%d-%m-%Y")
                        except ValueError:
                            try:
                                # Attempt to parse relative dates (e.g., "today", "next Monday") - basic implementation
                                if "today" in date_str.lower():
                                    target_date = datetime.datetime.now().strftime("%d-%m-%Y")
                                elif "next monday" in date_str.lower():
                                    today = datetime.datetime.now()
                                    days_until_monday = (7 - today.weekday() + 0) % 7
                                    next_monday = today + datetime.timedelta(days=days_until_monday)
                                    target_date = next_monday.strftime("%d-%m-%Y")
                                # Add more relative date parsing as needed
                            except:
                                pass

                if target_date:
                    client = pymongo.MongoClient(MONGO_URI)
                    db = client[DATABASE_NAME]
                    events_collection = db["college_events"]
                    events_on_day = []
                    for event in events_collection.find({"date": target_date}):
                        ug1 = event.get("ug1_event", None)
                        ug2_3 = event.get("ug2_3_event", None)
                        if ug1:
                            events_on_day.append(f"UG 1: {ug1}")
                        if ug2_3:
                            events_on_day.append(f"UG 2/3: {ug2_3}")

                    if events_on_day:
                        dispatcher.utter_message(text=f"On {format_date(target_date)}, the following events are scheduled:\n" + "\n".join(events_on_day))
                    else:
                        dispatcher.utter_message(text=f"There are no specific college events listed for {format_date(target_date)}.")
                else:
                    dispatcher.utter_message(text=f"Sorry, I couldn't understand the date you provided.")

            except pymongo.errors.ConnectionFailure as e:
                print(f"Error connecting to MongoDB: {e}")
                dispatcher.utter_message(text="Sorry, I'm having trouble connecting to the database.")
            except Exception as e:
                print(f"Error fetching events by date: {e}")
                dispatcher.utter_message(text="Sorry, there was an error retrieving events for that date.")

            finally:
                if 'client' in locals() and client:
                    client.close()
        else:
            dispatcher.utter_message(text="Please specify the date for which you want to know the events.")

        return []

class ActionShowFestivalOnDate(Action):
    def name(self) -> Text:
        return "action_show_festival_on_date"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        date_str = tracker.get_slot("date")
        month_str = tracker.get_slot("month")

        if date_str:
            try:
                target_date = None
                try:
                    target_date_obj = datetime.datetime.strptime(date_str, "%d-%m-%Y")
                    target_date_formatted = target_date_obj.strftime("%d-%b-%y")
                except ValueError:
                    try:
                        target_date_obj = datetime.datetime.strptime(date_str, "%d %B")
                        target_date_formatted = target_date_obj.strftime("%d-%b-%y")
                    except ValueError:
                        try:
                            target_date_obj = datetime.datetime.strptime(date_str, "%B %d, %Y")
                            target_date_formatted = target_date_obj.strftime("%d-%b-%y")
                        except ValueError:
                            dispatcher.utter_message(text=f"Sorry, I couldn't understand the date you provided.")
                            return []

                if target_date_formatted:
                    client = pymongo.MongoClient(MONGO_URI)
                    db = client[DATABASE_NAME]
                    festivals_collection = db["festivals_special_days"]
                    festival_found = None
                    for month_data in festivals_collection.find():
                        for day_event in month_data.get(list(month_data.keys())[0], []):
                            if day_event.get("date", "").lower() == target_date_formatted.lower():
                                festival_found = day_event.get("event")
                                break
                        if festival_found:
                            break

                    if festival_found:
                        dispatcher.utter_message(text=f"On {format_date(date_str)}, the following festival or special day is observed: {festival_found}")
                    else:
                        dispatcher.utter_message(text=f"There are no specific festivals or special days listed for {format_date(date_str)}.")

            except pymongo.errors.ConnectionFailure as e:
                print(f"Error connecting to MongoDB: {e}")
                dispatcher.utter_message(text="Sorry, I'm having trouble connecting to the database.")
            except Exception as e:
                print(f"Error fetching festival by date: {e}")
                dispatcher.utter_message(text="Sorry, there was an error retrieving the festival for that date.")

            finally:
                if 'client' in locals() and client:
                    client.close()
        elif month_str:
            try:
                client = pymongo.MongoClient(MONGO_URI)
                db = client[DATABASE_NAME]
                festivals_collection = db["festivals_special_days"]
                festivals_in_month = []
                for month_data in festivals_collection.find():
                    month_name = list(month_data.keys())[0]
                    if month_name.lower() == month_str.lower():
                        for day_event in month_data.get(month_name, []):
                            festivals_in_month.append(f"{day_event.get('date', 'N/A')} ({day_event.get('day', 'N/A')}): {day_event.get('event', 'N/A')}")
                        break

                if festivals_in_month:
                    dispatcher.utter_message(text=f"In {month_str.capitalize()}, the following festivals and special days are observed:\n" + "\n".join(festivals_in_month))
                else:
                    dispatcher.utter_message(text=f"There are no specific festivals or special days listed for {month_str.capitalize()}.")

            except pymongo.errors.ConnectionFailure as e:
                print(f"Error connecting to MongoDB: {e}")
                dispatcher.utter_message(text="Sorry, I'm having trouble connecting to the database.")
            except Exception as e:
                print(f"Error fetching festivals by month: {e}")
                dispatcher.utter_message(text="Sorry, there was an error retrieving the festivals for that month.")

            finally:
                if 'client' in locals() and client:
                    client.close()
        else:
            dispatcher.utter_message(text="Please specify the date or month for which you want to know the festivals or special days.")

        return []