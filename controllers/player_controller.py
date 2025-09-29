from models import player_model
from views.views import PlayerView
from models.player_model import Player
import os
import json

class PlayerController:

    def __init__(self, player, view):
        self.player = player
        self.view = view

    def add_player(self):
        """Ask user input to create and add a new player"""
        first_name = self.view.ask_first_name()
        last_name = self.view.ask_last_name()
        birth_date = self.view.ask_birth_date()
        national_id = self.view.ask_national_id()
        ranking = self.view.ask_ranking()

        new_player = player_model.Player(first_name, last_name, birth_date, national_id, ranking)
        self.player.append(new_player)
        new_player.save_to_json()
        return new_player

    def show_all_players(self):
        """Display all players alphabetically (loaded from JSON files in data/players)"""
        folder_path = "./data/players/"

        loaded_players = []

        if os.path.exists(folder_path):
            for filename in os.listdir(folder_path):
                if filename.endswith(".json"):
                    file_path = os.path.join(folder_path, filename)
                    with open(file_path, "r", encoding="utf-8") as f:
                        try:
                            player_data = json.load(f)
                            # Recreate a Player object
                            player = Player(
                                first_name=player_data["first_name"],
                                last_name=player_data["last_name"],
                                birth_date=player_data["birth_date"],
                                national_id=player_data["national_id"],
                                ranking=player_data["ranking"],
                            )
                            loaded_players.append(player)
                            self.view.display_all_players(loaded_players)
                        except json.JSONDecodeError:
                            print(f"Error reading file {filename}")


"""
    def show_all_players(self):
        Display all players alphabetically
        #To do - Récuperer les joueurs depuis les fichiers json
        self.view.display_all_players(self.player)
        """
        