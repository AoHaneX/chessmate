from models import tournament_model
from views.views import TournamentView
from models.tournament_model import Tournament
from utils.json_manager import update_jsons, get_data_from_file
import os
import json


class TournamentController:
    def __init__(self, tournament, view, player_manager):
        self.tournament = tournament
        self.view = view
        self.player_manager = player_manager
        self.all_players = None  # To be set when managing players

    def create_tournament(self):
        """Create a new tournament"""
        name = self.view.ask_tournament_name()
        location = self.view.ask_tournament_location()
        start_date = self.view.ask_start_date()
        end_date = self.view.ask_end_date()
        description = self.view.ask_description()
        rounds = self.view.ask_round()
        status = "Not Started"
        new_tournament = tournament_model.Tournament(name, location, start_date, end_date, description, rounds, status)
        new_tournament.save_to_json()
        return new_tournament

    def _get_tournament_path(self):
        #name = self.tournament.name.replace(" ", "_")
        return f"./data/tournaments/tournament_{self.tournament.name}_.json"

    def manage_tournament(self, tournament):
        while True:
            self.view.display_management_menu(tournament)
            choice = self.view.ask_management_choice()

            if choice == "1":
                # Display tournament info
                self.show_tournament_info(tournament)

            elif choice == "2":
                # Manage players
                self.manage_players(tournament)

            elif choice == "3":
                # Show players by score
                self.show_players(tournament, by_score=True)
                
            elif choice == "4":
                # Manage rounds
                print("To be implemented")

            elif choice == "0":
                print("Returning to main menu...")
                break

            else:
                print("Invalid choice. Try again.")

    def manage_players(self, tournament):
        while True:
            print("\n--- Player Management ---")
            print("1. Add player to tournament")
            print("2. Show tournament players")
            print("0. Back")

            choice = input("Your choice: ")

            if choice == "1":
                self.register_player()

            elif choice == "2":
                self.show_players(tournament=self.tournament)

            elif choice == "0":
                break

    def register_player(self):
        """Display the list of available players, allow user to select one,
    and add them to the tournament if not already registered."""
        print("\nAvailable Players:")
        if self.all_players is None:
            self.all_players = self.player_manager.get_all_players()
        if not self.all_players:
            print("No available players found.")
            return
        for i, p in enumerate(self.all_players, start=1):
            print(f"{i}. {p.first_name} {p.last_name} ({p.national_id})")
        pid = input("Enter national_id of the player to add: ")
        player = next((pl for pl in self.all_players if pl.national_id == pid), None)
        if not player:
            print("Player not found")
            
        player_dict = player.to_dict()
        if any(p["national_id"] == player_dict["national_id"] for p in self.tournament.players):
            print(f"Player {player.first_name} {player.last_name} is already registered.")
            return       
        self.tournament.players.append(player.to_dict())
        print("JOUEEEEUR:", self.tournament.players)
        self.save_tournament(self.tournament.name)

        print(f"Player {player.first_name} {player.last_name} added to tournament '{self.tournament.name}'.")

    def show_tournament_info(self, tournament):
        """Display basic tournament info"""
        self.view.display_tournament(tournament)

    def show_players(self, tournament, by_score=False):
        """
        Display tournament players
        """
        #Convert dict to Player objects if necessary
        player_object = []
        for p in tournament.players:
            if hasattr(p, "last_name"):
                player_object.append(p)
            elif isinstance(p, dict):
                # Adapter selon la signature de Player
                player_object.append(self.player_manager.dict_to_player(p))
            else:
                print("Unknown player format:", p)
        
        if by_score:
            self.view.display_players_by_score(tournament, players=player_object)
        else:
            self.view.display_players(tournament, players=player_object)

    def add_round(self, round_obj):
        """Add a round to the tournament"""
        self.tournament.add_round(round_obj)

    def current_round(self):
        """Return the current round object, or None if none exists"""
        if self.tournament.rounds:
            return self.tournament.rounds[-1]
        return None

    def is_finished(self):
        """Check if the tournament is finished"""
        return self.tournament.is_finished()

    def get_all_tournaments(self):
        """Load all tournaments from JSON files and return them"""
        folder_path = "./data/tournaments/"
        loaded_tournaments = []

        if os.path.exists(folder_path):
            for filename in os.listdir(folder_path):
                if filename.endswith(".json"):
                    file_path = os.path.join(folder_path, filename)
                    with open(file_path, "r", encoding="utf-8") as f:
                        try:
                            tournament_data = json.load(f)
                            if isinstance(tournament_data, list):
                                print("Tournament data is a list, expected a dict. Skipping.")
                                #To DO- Transform list to dict
                            elif isinstance(tournament_data, dict):
                                tournament = Tournament(
                                    name=tournament_data["name"],
                                    location=tournament_data["location"],
                                    start_date=tournament_data["start_date"],
                                    end_date=tournament_data.get("end_date", None),
                                    number_of_rounds=tournament_data.get("number_of_rounds", 4),
                                    description=tournament_data.get("description", "")
                                )
                                tournament.status = tournament_data.get("status")
                                tournament.current_round = tournament_data.get("current_round", 0)
                                tournament.players = tournament_data.get("players", [])
                                tournament.rounds = tournament_data.get("rounds", [])
                                loaded_tournaments.append(tournament)    
                                                      
                        except json.JSONDecodeError:
                            print(f"Error reading file {filename}")
                            
            return loaded_tournaments

    def show_all_tournaments(self, tournaments):
        """Display the given list of tournaments using the view"""
        print("======List of Tournaments======")
        for t in tournaments:
            self.view.display_tournament(t)

    def show_all_tournaments_with_index(self, tournaments):
        """Display the given list of tournaments using the view"""
        print("======List of Tournaments======")
        for i, t in enumerate(tournaments, start=1):
            simple = self.view.display_tournament_simplified(t)           
            print(f"{i}. {simple}")

    def save_tournament(self, name):
        file_path = self._get_tournament_path()
        tournaments = get_data_from_file(file_path)
        # Check if the tournament already exists
        updated = False
        if not tournaments:
            print("No tournaments found")
            return
        for t in tournaments:
            if isinstance(t, dict) and t.get("name") == self.tournament.name:
                t.update()
            updated = True

        if not updated:
            tournaments.append(self.tournament.to_dict())

        update_jsons(file_path, tournaments)

    def save_to_json(self):
        file_path = self._get_tournament_path()
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

    