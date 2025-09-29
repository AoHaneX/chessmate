from models import tournament_model
from views.views import TournamentView

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

        new_tournament = tournament_model.Tournament(name, location, start_date, end_date, description)
        self.tournament.append(new_tournament)
        new_tournament.save_to_json()
        return new_tournament
    
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
