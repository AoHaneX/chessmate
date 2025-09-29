from models import tournament_model
from views.views import TournamentView
from models.tournament_model import Tournament
import os
import json
class TournamentController:

    def __init__(self, tournament, view):
        self.tournament = tournament
        self.view = view

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
        self.tournament.append(new_tournament)
        new_tournament.save_to_json()
        return new_tournament
    
    def manage_tournament(self):
        while True:
            self.view.display_management_menu(self.tournament)
            choice = self.view.ask_management_choice()

            if choice == "1":
                self.show_tournament_info()

            elif choice == "2":
                self.show_players(by_score=False)

            elif choice == "3":
                self.show_players(by_score=True)

            elif choice == "4":
                print("➡️ Add round: to be implemented")

            elif choice == "5":
                self.view.display_rounds(self.tournament)

            elif choice == "0":
                print("Returning to main menu...")
                break

            else:
                print("⚠️ Invalid choice. Try again.")

    # --- méthodes déjà existantes ---
    def show_tournament_info(self):
        self.view.display_tournament(self.tournament)

    def show_players(self, by_score=False):
        if by_score:
            self.view.display_players_by_score(self.tournament)
        else:
            self.view.display_players(self.tournament)
    def add_player(self, player):
        """Add a player to the tournament"""
        self.tournament.add_player(player)

    def show_tournament_info(self):
        """Display basic tournament info"""
        self.view.display_tournament(self.tournament)

    def show_players(self, by_score=False):
        """Display tournament players"""
        if by_score:
            self.view.display_players_by_score(self.tournament)
        else:
            self.view.display_players(self.tournament)

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
                            status_order = {"Not Started": 0, "In Progress": 1, "Finished": 2}

                            loaded_tournaments.sort(
                                key=lambda t: status_order.get(getattr(t, "status", "Not Started"), 99)
                            )
                            
                            loaded_tournaments.append(tournament)
                        except json.JSONDecodeError:
                            print(f"Error reading file {filename}")
            return loaded_tournaments
                    
    def show_all_tournaments(self, tournaments):
            """Display the given list of tournaments using the view"""
            for t in tournaments:
                self.view.display_tournament(t) 
    def show_all_tournaments_with_index(self, tournaments):
        """Display the given list of tournaments using the view"""
        for i, t in enumerate(tournaments, start=1):
            simple = self.view.display_tournament_simplified(t)
            print(f"{i}. {simple}")
