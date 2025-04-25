# action.py
import json
import os
from typing import Any, Text, Dict, List
from pymongo import MongoClient
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa.actions.compliance.naac_data import get_naac_info  # Import the new function

class ActionFetchNaacInfo(Action):
    def name(self) -> Text:
        return "action_fetch_naac_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the NAAC info using the new function
        message = get_naac_info()
        dispatcher.utter_message(text=message)
        return []
