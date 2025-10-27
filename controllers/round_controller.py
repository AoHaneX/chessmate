from models import round_model
from views.views import RoundView


class RoundController:

    def __init__(self, round_obj, view, tournament):
        self.round = round_obj
        self.view = view
        self.tournament = tournament

    def add_match(self, match):
        """Add a match to the round"""
        self.round.add_match(match)

    def finish_round(self):
        """Finish the round with user-provided end date"""
        end_date = self.view.ask_end_date()
        self.round.finish_round(end_date)

    def show_round(self):
        """Display round info and matches"""
        self.view.display_round(self.round)
        self.view.display_matches(self.round)
