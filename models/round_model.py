from datetime import datetime
import os
import json


class Round:
    def __init__(self, name):
        self.name = name
        self.start_date = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.end_date = None
        self.list_matches = []  # list of Match objects
        self.matches = self.list_matches  # <-- compatibility alias used elsewhere in the code
        self.status = "ongoing"

    def add_match(self, match):
        """Add a Match object to the round"""
        self.list_matches.append(match)

    def finish_round_now(self):
        """Mark the round as finished with current date and hour"""
        self.end_date = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.status = "finished"
        
    def finish_round(self, end_date):
        """Mark the round as finished with a precise date and hour(String format: DD/MM/YYYY HH:MM)"""
        self.end_date = end_date
        self.status = "finished"

    def __str__(self):
        return f"{self.name} ({self.status})"

    def to_dict(self):
        return {
            "name": self.name,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "status": self.status,
            "matches": [
                {
                    "player1": match.player1.national_id,
                    "player2": match.player2.national_id,
                    "score1": match.score1,
                    "score2": match.score2
                }
                for match in self.list_matches
            ]
        }
    #Not mean to use because each round is linked to a tournament
    def save_to_json(self):
        name="round_data" + self.name + "_" + str(self.start_date) + ".json"
        file_path = "./data/" + name
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        round_data = {
                "name": self.name,
                "start_date": self.start_date,
                "end_date": self.end_date,
                "status": self.status
                }
        with open(file_path, 'w') as json_file:
            json.dump(round_data, json_file)