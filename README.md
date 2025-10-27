========================================
   CHESS TOURNAMENT MANAGER ♟️
========================================

A Python console-based application to manage chess tournaments, 
following the MVC (Model-View-Controller) architecture.

The program works fully offline and uses JSON files 
to save and load tournament data.


----------------------------------------
🚀 MAIN FEATURES
----------------------------------------

- Manage players:
  • Add new players (with national ID)
  • Display all players alphabetically

- Manage tournaments:
  • Create and edit tournaments
  • Set location, date, number of rounds, and description
  • Automatically save tournaments in JSON format

- Manage rounds and matches:
  • Round-robin pairing (every player meets all others)
  • Record match results and player scores
  • Display current standings

- Data persistence:
  • All data stored in /data/players.json and /data/tournaments/

- Code quality:
  • PEP8 compliant
  • Checked with flake8 and flake8-html


----------------------------------------
🧩 PROJECT STRUCTURE
----------------------------------------

ProjetEchec/
│
├── controllers/
│   ├── player_controller.py
│   ├── tournament_controller.py
│   ├── round_controller.py
│   └── match_controller.py
│
├── models/
│   ├── player_model.py
│   ├── tournament_model.py
│   ├── round_model.py
│   └── match_model.py
│
├── views/
│   └── views.py
│
├── data/
│   ├── players.json
│   └── tournaments/
│       └── <tournament_name>.json
│
├── main.py
└── requirements.txt


----------------------------------------
⚙️ INSTALLATION
----------------------------------------

1. Clone this repository:
   > git clone https://github.com/your-username/ProjetEchec.git
   > cd ProjetEchec

2. Create and activate a virtual environment:
   > python -m venv env
   > env\Scripts\activate     (on Windows)
   > source env/bin/activate  (on Mac/Linux)

3. Install dependencies:
   > pip install -r requirements.txt


----------------------------------------
▶️ HOW TO RUN THE PROGRAM
----------------------------------------

Launch the application:
   > python main.py

The main menu will let you:
   • Manage players
   • Create and start tournaments
   • Generate rounds and enter results
   • Display reports and standings


----------------------------------------
🧹 CODE QUALITY CHECK (FLAKE8)
----------------------------------------

To check code style compliance (PEP8):

   > flake8 --format=html --htmldir=flake8_report

This will generate an HTML report inside the folder:
   /flake8_report/index.html

You can open this file in any browser to review 
the linting results and ensure the code is clean.


----------------------------------------
📄 AUTHOR
----------------------------------------
Developed as part of the OpenClassrooms "Développeur d'application Python"

Author: STALIN--RENAULT Adrian
Year: 2025
