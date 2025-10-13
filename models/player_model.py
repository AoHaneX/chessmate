import os
import json

class Player:
    def __init__(self, first_name, last_name, birth_date, national_id, ranking=1000):

        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date  # (format: DD/MM/YYYY)
        self.national_id = national_id
        self.ranking = ranking
        self.score = 0  # To do score accumulated in a tournament - Quand initialiser  il faut reset le score

    def __str__(self):
        return f"{self.first_name} {self.last_name} (ID: {self.national_id}, Ranking: {self.ranking}, Score: {self.score})"

    def save_to_json(self):
        name = "player_" + self.last_name + "_" + self.first_name + ".json"
        file_path = "./data/players/" + name
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        player_data = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birth_date": self.birth_date,
            "national_id": self.national_id,
             "ranking": self.ranking,
             "score": self.score
         }
        with open(file_path, 'w') as json_file:
            json.dump(player_data, json_file)
    
    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birth_date": self.birth_date,
            "national_id": self.national_id,
            "ranking": self.ranking
        }

    def dict_to_player(self, player_dict):
        """
        Convert a dictionary to a Player object.
        """
        return Player(
            first_name=player_dict["first_name"],
            last_name=player_dict["last_name"],
            birth_date=player_dict["birth_date"],
            national_id=player_dict["national_id"],
            ranking=player_dict.get("ranking", 0)
        )
