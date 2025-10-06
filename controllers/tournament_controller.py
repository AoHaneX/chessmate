from models import tournament_model
from views.views import TournamentView
from models.tournament_model import Tournament
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

    def manage_tournament(self, tournament):
        while True:
            self.view.display_management_menu(tournament)
            choice = self.view.ask_management_choice()

            if choice == "1":
                # Display tournament info
                self.show_tournament_info(tournament)

            elif choice == "2":
                # Manage players
                self.manage_players()

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

    def manage_players(self):
        while True:
            print("\n--- Player Management ---")
            print("1. Add player to tournament")
            print("2. Show tournament players")
            print("0. Back")

            choice = input("Your choice: ")

            if choice == "1":
                print("\nAvailable Players:")
                if self.all_players is None:
                    self.all_players = self.player_manager.get_all_players()
                    for i, p in enumerate(self.all_players, start=1):
                        print(f"{i}. {p.first_name} {p.last_name} ({p.national_id})")

                pid = input("Enter national_id of the player to add: ")
                player = next((pl for pl in self.all_players if pl.national_id == pid), None)                  
                if player:
                    self.tournament.register_player(player)
                    self.all_players.remove(player)
                    print(f"Player {player.first_name} {player.last_name} added.")
                else:
                    print("Player not found.")
                self.save_tournament(self.tournament.name)

            elif choice == "2":
                self.show_players(tournament=self.tournament)

            elif choice == "0":
                break

    def register_player(self, player):
        print("PLAAAAAYAAAAAAAAAAAAAAAa")
        """Add a player to the tournament"""

    def show_tournament_info(self, tournament):
        """Display basic tournament info"""
        self.view.display_tournament(tournament)

    def show_players(self, tournament, by_score=False):
        """Display tournament players"""
        
        #To do
        if by_score:
            self.view.display_players_by_score(tournament)
        else:
            self.view.display_players(tournament)

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
                            tournament = Tournament(
                                name=tournament_data["name"],
                                location=tournament_data["location"],
                                start_date=tournament_data["start_date"],
                                end_date=tournament_data.get("end_date", None),
                                number_of_rounds=tournament_data.get("number_of_rounds", 4),
                                description=tournament_data.get("description", "")
                            )
                            loaded_tournaments.append(tournament)
                            status_order = {"Not Started": 0, "In Progress": 1, "Finished": 2}
                            loaded_tournaments.sort(
                                key=lambda t: status_order.get(getattr(t, "status", "Not Started"), 99)
                            )                         
                            tournament.status = tournament_data.get("status", "Not Started")
                            print("DEBUG loaded:", [t.name for t in loaded_tournaments])
                            
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
        name = "tournament_" + name + "_" + ".json"
        print("Le nom du tournoi est : ", name)
        file_path = "./data/tournaments/" + name
        tournaments = self.get_data(file_path)

        # Check if the tournament already exists
        updated = False
        for t in tournaments:
            if t["name"] == self.tournament.name:
                t.update(self.tournament.to_dict())
                updated = True
                break

        if not updated:
            tournaments.append(self.tournament.to_dict())

        self.update_jsons(file_path, tournaments)
