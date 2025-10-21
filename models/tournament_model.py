import json
import os
from .round_model import Round


class Tournament:
    def __init__(
        self,
        name,
        location,
        start_date,
        end_date,
        number_of_rounds=4,
        description="",
        status="Not started",
        players=None,
    ):
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.number_of_rounds = number_of_rounds
        self.rounds = []  # list of Round objects
        self.players = []  # list of Player objects
        # To do- Vérifier où et comment gérer les scores
        # Is finish or not
        self.description = description
        self.status = status  # "Not Started", "In Progress", "Finished"
        self.players = players if players is not None else []

    def to_dict(self):
        """Return a JSON-serializable dict including rounds (each round uses Round.to_dict())."""
        players_serialized = []
        for p in self.players:
            if isinstance(p, str):
                players_serialized.append(p)
            elif isinstance(p, dict):
                players_serialized.append(p.get("national_id", p))
            else:
                players_serialized.append(getattr(p, "national_id", str(p)))

        # Serialize rounds using Round.to_dict() when available
        rounds_serialized = []
        for r in self.rounds:
            try:
                rounds_serialized.append(r.to_dict())
            except Exception:
                rounds_serialized.append(r)  # fallback: si c'est déjà dict ou une structure simple

        return {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "number_of_rounds": self.number_of_rounds,
            "rounds": rounds_serialized,
            "players": players_serialized,
            "description": self.description,
            "status": self.status,
        }

    @staticmethod
    def from_dict(data: dict) -> "Tournament":
        tournament = Tournament(
            name=data.get("name"),
            location=data.get("location"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            number_of_rounds=data.get("number_of_rounds", 0),
            description=data.get("description", ""),
            status=data.get("status", "Not started"),
            players=data.get("players", []),
        )
        # Reconstruire les rounds à partir du JSON
        tournament.rounds = [Round(
            name=r["name"],
            # facultatif : garde les dates et status
            ) for r in data.get("rounds", [])
        ]
        return tournament
    
    def save_to_json(self):
        """Write the tournament (including rounds) to disk as JSON."""
        file_path = f"./data/tournaments/tournament_{self.name}_.json"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=4)