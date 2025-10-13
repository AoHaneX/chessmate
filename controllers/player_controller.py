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
    
    def register_player(self, player):
        """Register a player to the controller's player list"""
        self.player.append(player)  
      
    def get_all_players(self):
        """Load all players from JSON files and return them sorted alphabetically"""
        folder_path = "./data/players/"
        loaded_players = []

        if os.path.exists(folder_path):
            for filename in os.listdir(folder_path):
                if filename.endswith(".json"):
                    file_path = os.path.join(folder_path, filename)
                    with open(file_path, "r", encoding="utf-8") as f:
                        try:
                            player_data = json.load(f)
                            player = Player(
                                first_name=player_data["first_name"],
                                last_name=player_data["last_name"],
                                birth_date=player_data["birth_date"],
                                national_id=player_data["national_id"],
                                ranking=player_data["ranking"],
                            )
                            loaded_players.append(player)
                        except json.JSONDecodeError:
                            print(f"⚠️ Error reading file {filename}")

        # Sort players alphabetically by last name, then first name
        loaded_players.sort(key=lambda p: (p.last_name.lower(), p.first_name.lower()))

        return loaded_players

    def show_all_players(self, players):
        """Display the given list of players using the view"""
        self.view.display_all_players(players)
    