# Chess Tournament Manager ♟️

A Python console-based application to manage chess tournaments, following the **MVC architecture**.  
The program is standalone, offline, and uses JSON files for data persistence.

---

## 🚀 Features

- Manage a **list of players** stored in `data/players.json`
  - Add players (with national chess ID)
  - Display players in alphabetical order
- Manage **tournaments** stored in `data/tournaments.json`
  - Tournament information (name, location, dates, description)
  - Number of rounds (default = 4)
  - Rounds and matches
- **Swiss system pairing** (simplified)
  - First round: random shuffle
  - Next rounds: pair players based on their scores
  - Avoid repeated pairings
- Match results:
  - Win = 1 point
  - Draw = 0.5 point each
  - Loss = 0 point
- Reports:
  - List of all players
  - List of tournaments
  - Tournament details (rounds, matches, players)
- Data persistence:
  - Automatic save and load from JSON files
- Code quality:
  - Follows **PEP8** style guide
  - Checked with **flake8**
  - HTML report generated with **flake8-html**

---

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/ProjetEchec.git
   cd ProjetEchec
