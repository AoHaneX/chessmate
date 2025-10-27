import random
from models import tournament_model
from models.round_model import Round
from views.views import TournamentView
from models.tournament_model import Tournament
from models.player_model import Player
from models.match_model import Match
from utils.json_manager import update_jsons
import os
import json


class TournamentController:
    def __init__(self, tournament, view, player_manager):
        self.tournament = tournament
        self.view = view
        self.player_manager = player_manager
        self.all_players = None  # To be set when managing players
        self.rounds_generated = False
        self.number_of_rounds = 0

    def create_tournament(self):
        """Create a new tournament"""
        name = self.view.ask_tournament_name()
        location = self.view.ask_tournament_location()
        start_date = self.view.ask_start_date()
        end_date = self.view.ask_end_date()
        description = self.view.ask_description()
        status = "Not Started"
        new_tournament = tournament_model.Tournament(name, location, start_date, end_date, description, status)
        new_tournament.save_to_json()
        return new_tournament

    def _get_tournament_path(self):
        # name = self.tournament.name.replace(" ", "_")
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
                # Show players by alphabetical order
                self.show_players(tournament=self.tournament)

            elif choice == "4":
                # Manage rounds
                self.manage_rounds(tournament)

            elif choice == "0":
                print("Returning to main menu...")
                break

            else:
                print("Invalid choice. Try again.")

    def manage_players(self, tournament):
        while True:
            choice = self.view.manage_player(tournament)

            if choice == "1":
                self.register_player()

            elif choice == "2":
                self.show_players(tournament=self.tournament)

            elif choice == "0":
                break

    def manage_rounds(self, tournament):
        while True:
            choice = self.view.ask_round_management_choice()

            if choice == "1":
                # Generate rounds and matches
                if self.rounds_generated:
                    print("Rounds have already been generated.")
                else:
                    self.create_rounds_from_pairs(tournament)
            elif choice == "2":
                # Show all existing rounds
                self.view.display_rounds(tournament)

            elif choice == "3":
                # Show matches of a selected round
                if not tournament.rounds:
                    print("No rounds available yet.")
                    continue
                self.view.display_rounds(tournament)
                try:
                    round_index = int(input("Enter the round number to display: ")) - 1
                    if 0 <= round_index < len(tournament.rounds):
                        round_obj = tournament.rounds[round_index]
                        self.view.display_matches(round_obj)
                    else:
                        print("Invalid round number.")
                except ValueError:
                    print("Please enter a valid number.")

            elif choice == "4":
                # Record results for a round
                self.enter_match_results(tournament)
                self.save_tournament(self.tournament.name)

            elif choice == "5":
                # Show standings
                self.show_current_standings(tournament)

            elif choice == "6":
                # Start tournament
                self.start_tournament(tournament)

            elif choice == "7":
                # End tournament
                self.end_tournament(tournament)

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
        pid = input("Enter national_id of the player to add: ").strip()
        player = next((pl for pl in self.all_players if pl.national_id == pid), None)
        if not player:
            print("Player not found")
            return
        if any(((p.get("national_id") 
                if isinstance(p, dict) 
                else getattr(p, "national_id", None) 
                if hasattr(p, "national_id") else str(p)) == player.national_id) for p in self.tournament.players):
            print("Player already registered in this tournament.")
            return
        if player is str:
            print("Invalid player format.")
            return
        self.tournament.players.append(player)
        self.save_tournament(self.tournament.name)

        print(f"Player {player.first_name} {player.last_name} added to tournament '{self.tournament.name}'.")

    def show_tournament_info(self, tournament):
        """Display basic tournament info"""
        self.view.display_tournament(tournament)

    def show_players(self, tournament):
        """
        Display tournament players
        """
        # Convert dict to Player objects if necessary
        player_object = []
        all_players = self.all_players or self.player_manager.get_all_players()
        for p in tournament.players:
            if hasattr(p, "last_name"):
                player_object.append(p)
            elif isinstance(p, dict):
                player_object.append(Player(**p))
            else:
                found = next((pl for pl in all_players if pl.national_id == str(p)), None)
                if found:
                    player_object.append(found)
                else:
                    print(f"Unknown player format: {p}")
            self.view.display_players(tournament, players=player_object)

    def add_round(self, round_obj):
        """Add a round to the tournament"""
        self.tournament.add_round(round_obj)
    
    def generate_round_and_pairs(self, players):
        pairs = []
        player_list = players.copy()
        total_players = len(player_list)
        if total_players % 2 != 0:
            player_list.append(None)
        random.shuffle(player_list)
        # Generate one round per player (minus one)
        for i in range(total_players - 1):
            round_pairs = []
            for j in range(total_players // 2):
                p1 = player_list[j]
                p2 = player_list[-j - 1]
                # Skip the "None" (bye) player
                if p1 is not None and p2 is not None:
                    round_pairs.append((p1, p2))
            pairs.append(round_pairs)
            player_list.insert(1, player_list.pop())
        self.save_tournament(self.tournament.name)
        return pairs

    def _to_player_obj(self, p):
        """Normalize a stored player entry into a Player object or None (for bye)."""
        # Already a Player
        if isinstance(p, Player):
            return p
        # Dict saved in JSON -> construct Player
        if isinstance(p, dict):
            try:
                return Player(**p)
            except TypeError:
                return None
        # Stored as national_id string -> lookup in available players
        if isinstance(p, str):
            all_players = self.all_players or self.player_manager.get_all_players()
            return next((pl for pl in all_players if pl.national_id == p), None)
        # None or unknown -> treat as bye
        return None

    def create_rounds_from_pairs(self, tournament):
        if self.rounds_generated is True:
            return
        self.rounds_generated = True

        # Normalize tournament.players into Player objects (or None for bye)
        players = [self._to_player_obj(p) for p in tournament.players]

        # If no players or insufficient players
        if not players:
            print("No players available to generate rounds.")
            return

        all_pairs = self.generate_round_and_pairs(players)
        for i, round_pairs in enumerate(all_pairs, start=1):
            tournament.number_of_rounds = i
            round_name = f"Round {i}"
            new_round = Round(name=round_name)
            for player1, player2 in round_pairs:
                # player1/player2 are already Player objects or None
                if player1 is None or player2 is None:
                    # Skip matches with a bye (or handle as desired)
                    continue
                match = Match(player1, player2)
                new_round.add_match(match)
            tournament.rounds.append(new_round)
        self.save_tournament(self.tournament.name)
        print(f"{len(tournament.rounds)} rounds successfully created.\n")

    def is_finished(self):
        """Check if the tournament is finished"""
        return self.tournament.is_finished()

    def get_all_tournaments(self):
        """Load all tournaments from JSON files, rebuild objects, and return them."""
        folder_path = "./data/tournaments/"
        loaded_tournaments = []

        if not os.path.exists(folder_path):
            return loaded_tournaments

        for filename in os.listdir(folder_path):
            if not filename.endswith(".json"):
                continue

            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    tournament_data = json.load(f)

                # Validate JSON structure
                if not isinstance(tournament_data, dict):
                    print(f"⚠ Tournament data in {filename} is not a dict. Skipped.")
                    continue

                # Create Tournament object
                tournament = Tournament(
                    name=tournament_data.get("name", "Unnamed"),
                    location=tournament_data.get("location", "Unknown"),
                    start_date=tournament_data.get("start_date", ""),
                    end_date=tournament_data.get("end_date"),
                    number_of_rounds=tournament_data.get("number_of_rounds", 0),
                    description=tournament_data.get("description", ""),
                    status=tournament_data.get("status", "Not started"),
                    players=[],
                )


                # Rebuild player objects
                players_data = tournament_data.get("players", [])
                all_players = self.player_manager.get_all_players()
                for p in players_data:
                    if isinstance(p, dict):
                        player_obj = Player(
                            first_name=p["first_name"],
                            last_name=p["last_name"],
                            birth_date=p["birth_date"],
                            national_id=p["national_id"],
                            ranking=p.get("ranking", 1000)
                        )
                        tournament.players.append(player_obj)
                    elif isinstance(p, str):
                        found = next((pl for pl in all_players if pl.national_id == p), None)
                        if found:
                            tournament.players.append(found)
                    else:
                        print(f"⚠ Unknown player format: {p}")

                # Rebuild round and match objects
                tournament.rounds = []
                for round_data in tournament_data.get("rounds", []):
                    if not isinstance(round_data, dict):
                        continue

                    round_obj = Round(name=round_data.get("name", "Unnamed Round"))
                    round_obj.start_date = round_data.get("start_date")
                    round_obj.end_date = round_data.get("end_date")
                    round_obj.status = round_data.get("status", "ongoing")

                    # Rebuild matches for each round
                    for match_data in round_data.get("matches", []):
                        p1 = None
                        p2 = None

                        # Find player1
                        if isinstance(match_data.get("player1"), str):
                            p1 = next((pl for pl in tournament.players if pl.national_id == match_data["player1"]), None)
                        elif isinstance(match_data.get("player1"), dict):
                            p1 = Player(**match_data["player1"])

                        # Find player2
                        if isinstance(match_data.get("player2"), str):
                            p2 = next((pl for pl in tournament.players if pl.national_id == match_data["player2"]), None)
                        elif isinstance(match_data.get("player2"), dict):
                            p2 = Player(**match_data["player2"])

                        # Create match object if both players exist
                        if p1 and p2:
                            match_obj = Match(
                                player1=p1,
                                player2=p2,
                                score1=match_data.get("score1", 0.0),
                                score2=match_data.get("score2", 0.0)
                            )
                            round_obj.add_match(match_obj)

                    tournament.rounds.append(round_obj)

                # Add tournament to loaded list
                loaded_tournaments.append(tournament)

            except Exception as e:
                print(f"Error reading file {filename}: {e}")

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
        update_jsons(file_path, self.tournament.to_dict())

    def enter_match_results(self, tournament):
        """Allow user to select a round and a match, then enter and save the match result."""

        if not tournament.rounds:
            print("No rounds available. Please generate rounds first.")
            return
        # Display available rounds
        print("\n=== Available Rounds ===")
        for i, rnd in enumerate(tournament.rounds, start=1):
            print(f"{i}. {rnd.name} | Status: {rnd.status}")
        print("========================")

        try:
            round_choice = int(input("Select a round number: "))
            if round_choice < 1 or round_choice > len(tournament.rounds):
                print("Invalid round number.")
                return
        except ValueError:
            print("Invalid input. Please enter a number.")
            return

        selected_round = tournament.rounds[round_choice - 1]

        # Display matches of selected round
        print(f"\n=== Matches in {selected_round.name} ===")
        for i, match in enumerate(selected_round.list_matches, start=1):
            print(f"{i}. {match.player1.first_name} {match.player1.last_name} "
                f"vs {match.player2.first_name} {match.player2.last_name} "
                f"({match.score1} - {match.score2})")
        try:
            match_choice = int(input("Select a match number: "))
            if match_choice < 1 or match_choice > len(selected_round.list_matches):
                print("Invalid match number.")
                return
        except ValueError:
            print("Invalid input. Please enter a number.")
            return

        selected_match = selected_round.list_matches[match_choice - 1]

        # Ask for result input
        print("\nEnter result (1-0, 0-1 or 0.5-0.5):")
        result_str = input("> ").strip()

        valid_results = {
            "1-0": (1.0, 0.0),
            "0-1": (0.0, 1.0),
            "0.5-0.5": (0.5, 0.5),
            "1/2-1/2": (0.5, 0.5)
        }

        if result_str not in valid_results:
            print("Invalid format. Use 1-0, 0-1 or 0.5-0.5.")
            return

        score1, score2 = valid_results[result_str]

        # Update match object
        selected_match.set_result(score1, score2)

        # Update players' scores
        self.update_player_scores(selected_match)

        # Save updated tournament
        tournament.save_to_json()
        print(f"Result saved for match: {selected_match.player1.last_name} vs {selected_match.player2.last_name}")
        print("Tournament file has been updated.")

    def update_player_scores(self, match):
        """Update both players' total scores after a match."""
        if hasattr(match.player1, "score"):
            match.player1.score += match.score1
        if hasattr(match.player2, "score"):
            match.player2.score += match.score2

    def show_current_standings(self, tournament):
        """Display the current player standings sorted by score and ranking."""
        if not tournament.players:
            print("No players available in this tournament.")
            return
        view = TournamentView()
        # Sort players by score (desc) then by ranking (desc)
        sorted_players = sorted(
            tournament.players,
            key=lambda p: (-p.score, -p.ranking)
        )
        view.display_standings(sorted_players)

    def start_tournament(self, tournament):
        """
        Start the tournament by updating its status and saving changes to JSON.
        """
        tournament.status = "Started"
        tournament.description = "The tournament has officially started."
        print(f"\nTournament '{tournament.name}' has been marked as Started.\n")
        try:
            self.save_tournament(tournament.name)
            print("Tournament data successfully saved to JSON.\n")
        except Exception as e:
            print(f"Error while saving tournament data: {e}")

    def end_tournament(self, tournament):
        """
        End the tournament by updating its status and saving changes to JSON.
        """
        tournament.status = "Ended"
        tournament.description = "The tournament has officially ended."
        print(f"\nTournament '{tournament.name}' has been marked as Ended.\n")
        try:
            self.save_tournament(tournament.name)
            print("Tournament data successfully saved to JSON.\n")
        except Exception as e:
            print(f"Error while saving tournament data: {e}")