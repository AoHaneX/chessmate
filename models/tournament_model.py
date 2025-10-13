import json
import os


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
        self.rounds = []  # list of Round objects
        self.players = []  # list of Player objects
        # To do- Vérifier où et comment gérer les scores
        # Is finish or not
        self.description = description
        self.status = status  # "Not Started", "In Progress", "Finished"
        self.players = players if players is not None else []

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
            "description": self.description,
            "status": self.status,
        }
       #Maybe change where it is
    def save_to_json(self):
        """Save tournament data to a JSON file"""
        file_path = self._get_tournament_path()
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        tournament_data = {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "number_of_rounds": self.number_of_rounds,
            "current_round": self.current_round,
            "rounds": ([round_obj.to_dict() for round_obj in self.rounds] if hasattr(self, 'rounds') and self.rounds else []),
            "players": [p.national_id for p in self.players] if hasattr(self, 'players') and self.players else [],
            "description": self.description,
            "status": self.status
        }
        with open(file_path, 'w', encoding="utf-8") as json_file:
            json.dump(tournament_data, json_file, indent=4, ensure_ascii=False)
        return file_path