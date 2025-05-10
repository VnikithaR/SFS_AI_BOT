from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pymongo
import datetime

# MongoDB configuration
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "sfs_infobot_db"

def format_date(date_str):
    """Format date into a more readable form."""
    for fmt in ("%d-%m-%Y", "%d-%b-%y", "%d %B", "%B %d, %Y"):
        try:
            return datetime.datetime.strptime(date_str, fmt).strftime("%B %d, %Y")
        except ValueError:
            continue
    return date_str  # Return original if parsing fails

def get_db_collection(collection_name):
    """Helper function to get MongoDB collection."""
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    return db[collection_name], client

# =================== ACTION: LIST COLLEGE EVENTS ===================

class ActionListCollegeEvents(Action):
    def name(self) -> Text:
        return "action_list_college_events"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            collection, client = get_db_collection("college_events")
            events_cursor = collection.find({})  # Get all events
            events_list = []

            for event in events_cursor:
                date_str = format_date(event.get("date", "N/A"))
                ug1 = event.get("ug1_event")
                ug2_3 = event.get("ug2_3_event")
                day = event.get("day", "N/A")
                event_info = f"{date_str} ({day}): "

                if ug1 and ug2_3:
                    event_info += f"UG 1 - {ug1}; UG 2/3 - {ug2_3}"
                elif ug1:
                    event_info += f"UG 1 - {ug1}"
                elif ug2_3:
                    event_info += f"UG 2/3 - {ug2_3}"
                else:
                    continue  # skip null entries
                events_list.append(event_info)

            if events_list:
                dispatcher.utter_message(text="Here are the upcoming college events:\n" + "\n".join(events_list))
            else:
                dispatcher.utter_message(text="No upcoming college events listed.")
        except Exception as e:
            print(f"Error: {e}")
            dispatcher.utter_message(text="There was an error fetching college events.")
        finally:
            client.close()

        return []

# =================== ACTION: SHOW EVENTS ON A SPECIFIC DATE ===================

class ActionShowEventOnDate(Action):
    def name(self) -> Text:
        return "action_show_event_on_date"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        date_str = tracker.get_slot("date")
        if not date_str:
            dispatcher.utter_message(text="Please specify a date.")
            return []

        try:
            for fmt in ("%d-%m-%Y", "%d %B", "%B %d, %Y"):
                try:
                    target_date = datetime.datetime.strptime(date_str, fmt).strftime("%d-%m-%Y")
                    break
                except ValueError:
                    continue
            else:
                if "today" in date_str.lower():
                    target_date = datetime.datetime.now().strftime("%d-%m-%Y")
                else:
                    dispatcher.utter_message(text="Could not understand the date provided.")
                    return []

            collection, client = get_db_collection("college_events")
            event = collection.find_one({"date": target_date})

            if event:
                messages = []
                if event.get("ug1_event"):
                    messages.append(f"UG 1: {event['ug1_event']}")
                if event.get("ug2_3_event"):
                    messages.append(f"UG 2/3: {event['ug2_3_event']}")
                if messages:
                    dispatcher.utter_message(text=f"Events on {format_date(target_date)}:\n" + "\n".join(messages))
                else:
                    dispatcher.utter_message(text=f"No specific events listed on {format_date(target_date)}.")
            else:
                dispatcher.utter_message(text=f"No events found on {format_date(target_date)}.")
        except Exception as e:
            print(f"Error: {e}")
            dispatcher.utter_message(text="There was an error fetching the events.")
        finally:
            client.close()

        return []

# =================== ACTION: SHOW FESTIVAL OR SPECIAL DAY ===================

class ActionShowFestivalOnDate(Action):
    def name(self) -> Text:
        return "action_show_festival_on_date"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        date_str = tracker.get_slot("date")
        month_str = tracker.get_slot("month")

        try:
            collection, client = get_db_collection("festivals_special_days")

            if date_str:
                for fmt in ("%d-%m-%Y", "%d-%b-%y", "%d %B", "%B %d, %Y"):
                    try:
                        date_obj = datetime.datetime.strptime(date_str, fmt)
                        formatted_date = date_obj.strftime("%d-%b-%y")
                        month_key = date_obj.strftime("%B %Y")
                        break
                    except ValueError:
                        continue
                else:
                    dispatcher.utter_message(text="Could not parse the date format.")
                    return []

                result = collection.find_one({month_key: {"$exists": True}})
                if result:
                    for event in result[month_key]:
                        if event.get("date") == formatted_date:
                            dispatcher.utter_message(
                                text=f"On {format_date(formatted_date)}, the festival/special day is: {event['event']}")
                            return []
                dispatcher.utter_message(text=f"No festival or special day found on {format_date(formatted_date)}.")

            elif month_str:
                month_key = month_str.strip().capitalize()
                festivals = []
                result = collection.find_one({month_key: {"$exists": True}})
                if result:
                    for event in result[month_key]:
                        festivals.append(f"{event.get('date')} ({event.get('day', 'N/A')}): {event.get('event')}")
                if festivals:
                    dispatcher.utter_message(text=f"Festivals in {month_key}:\n" + "\n".join(festivals))
                else:
                    dispatcher.utter_message(text=f"No festivals listed for {month_key}.")

            else:
                dispatcher.utter_message(text="Please specify a date or month.")

        except Exception as e:
            print(f"Error: {e}")
            dispatcher.utter_message(text="There was an error retrieving festival information.")
        finally:
            client.close()

        return []
