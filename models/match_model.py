import os
import json


class Match:
    def __init__(self, player1, player2, score1=0.0, score2=0.0):
        """Represents a chess match between two players."""
        self.player1 = player1
        self.player2 = player2
        self.score1 = score1
        self.score2 = score2

    def set_result(self, score1, score2):
        self.score1 = float(score1)
        self.score2 = float(score2)

    def __str__(self):
        return (f"{self.player1.first_name} {self.player1.last_name} ({self.score1}) "
                f"vs {self.player2.first_name} {self.player2.last_name} ({self.score2})")

    def save_to_json(self):
        name = "match_data" + self.player1.last_name + "_" + self.player2.last_name + ".json"
        file_path = "./data/" + name
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        round_data = {
                "player1": f"{self.player1.first_name} {self.player1.last_name}",
                "player2": f"{self.player2.first_name} {self.player2.last_name}",
                "score1": self.score1,
                "score2": self.score2
                }
        with open(file_path, 'w') as json_file:
            json.dump(round_data, json_file)
