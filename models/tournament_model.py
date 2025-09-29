from datetime import datetime
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


    def save_to_json(self):
        name="tournament_" + self.name + "_"  + ".json"
        file_path = "./data/tournaments/" + name
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        tournament_data = {
                "name": self.name,
                "location": self.location,
                "start_date": self.start_date,
                "end_date": self.end_date,
                "number_of_rounds": self.number_of_rounds,
                "current_round": self.current_round
                }
        with open(file_path, 'w') as json_file:
            json.dump(tournament_data, json_file)