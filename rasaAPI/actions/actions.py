# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

import json
from datetime import datetime as date
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from sqlalchemy import null


file = open("./actions/matches.json")
data = json.load(file)
print(data)
file.close()

class ActionShowSchedule(Action):
    def name(self) -> Text:
        return "action_show_schedule"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(f"Action: {self.name()}")

        reply = []
        for day in data['schedule']:
            reply.append(f"{day['name']}: {day['begins']} - {day['ends']}")
        dispatcher.utter_message(text=f"check out the schedule:\n{', '.join(reply)}")

        return []

class ActionShowAvailableGames(Action):
    def name(self) -> Text:
        return "action_show_available_games"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(f"Action: {self.name()}")

        reply = []
        for game in data['games']:
            if game['available']:
                reply.append(f"{game['name']}")
        dispatcher.utter_message(text=f"you can play one of those: {', '.join(reply)}")

        return []

class ActionAddToTournament(Action):
    def name(self) -> Text:
        return "action_add_to_tournament"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(f"Action: {self.name()}")

        error_reply = "sorry mate, it's already full"
        intent = str(tracker.get_intent_of_latest_message())

        if intent == "lol_game":
            game_name = "League of Legends"
        elif intent == "csgo_game":
            game_name = "Counter Strike: Global Offensive"
        elif intent == "fifa_game":
            game_name = "Fifa 22"
        else:
            dispatcher.utter_message(text="sorry mate, there is no tournament for your game")
            return []
        
        for game in data['games']:
            if game['name'] == game_name:
                if not game['available']:
                    dispatcher.utter_message(text="sorry mate, it's already full")
                    return []

                game['current_players'] += 1
                if game['current_players'] == game['max_players']:
                    game['available'] = False
                file = open("./actions/matches.json", "w")
                json.dump(data, file, indent=4, sort_keys=True)
                file.close()

                day_name = date.today().strftime("%A")
                for day in data['schedule']:
                    if day['name'] == day_name:
                        start_time = day['begins']
                        break

                reply = f"are you good and prepared, young chum? the tournament begins at {start_time}:00!\n"
                reply += f"you are #{game['current_players']} on list"
                dispatcher.utter_message(text=reply)
                return []
