from datetime import datetime
import json
import os
from pkgutil import get_data

class Tournament:
    def __init__(
        self,
        name,
        location,
        start_date,
        end_date,
        number_of_rounds=4,
        description="",
        status="Not started",
        players=None,
    ):
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.number_of_rounds = number_of_rounds
        self.current_round = 0
        self.list_rounds = []  # list of Round objects
        self.list_players = []  # list of Player objects
        #To do- Vérifier où et comment gérer les scores
        #Is finish or not
        self.description = description
        self.status = status  # "Not Started", "In Progress", "Finished"
        self.players = players if players is not None else []

    def save_to_json(self):
        name = "tournament_" + self.name + "_" + ".json"
        file_path = "./data/tournaments/" + name
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        tournament_data = {
                "name": self.name,
                "location": self.location,
                "start_date": self.start_date,
                "end_date": self.end_date,
                "number_of_rounds": self.number_of_rounds,
                "description": self.description,
                "current_round": self.current_round,
                "status": self.status
                }
        with open(file_path, 'w') as json_file:
            json.dump(tournament_data, json_file)

    def to_dict(self):
        """Convert tournament object to dict"""
        return {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "number_of_rounds": self.number_of_rounds,
            "current_round": self.current_round,
            "rounds": [round_obj.to_dict() for round_obj in self.rounds],
            "players": [p.national_id for p in self.players],
            "scores": self.scores,
            "description": self.description,
            "status": self.status,
        }

    def update_jsons(file_path, data):
        """Update the JSON file at the given path with the provided data"""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)

    def get_data_from_file(file_path):
        """
        Load data from a JSON file and return it as a dict or list. Return an empty list if the file does not exist or is empty.
        """
        if not os.path.exists(file_path):
            return []

        with open(file_path, "r", encoding="utf-8") as json_file:
            try:
                return json.load(json_file)
            except json.JSONDecodeError:
                return []

