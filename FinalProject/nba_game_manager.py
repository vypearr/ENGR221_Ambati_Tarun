"""
Author: Alex Perez and Tarun Ambati
Last updated: August 9, 2026
Description: Loads NBA game and team data from CSV files and stores
the records in dictionaries. Supports insert, delete, search, and
traverse operations.
"""

import pandas as pd

from game_record import GameRecord
from team_record import TeamRecord


class NBA_Game_Manager:
    """ Stores and manages NBA game and team records."""

    def __init__(self):
        """ Create empty dictionaries for games and teams."""

        # Keys are game IDs and values are GameRecord objects
        self.game_dict = {}

        # Keys are team abbreviations and values are TeamRecord objects
        self.team_dict = {}

    def import_games(self, filename):
        """Read game data from a CSV file and add it to game_dict."""

        # Read the game CSV file.
        game_data = pd.read_csv(filename)

        # Create one GameRecord object for every row
        game_data.apply(
            lambda row: self.add_game_from_row(row),
            axis=1
        )

    def add_game_from_row(self, row):
        """Create a GameRecord from one row of the game DataFrame."""

        # Create a game object using the row data.
        game = GameRecord(
            row["game_id"],
            row["season_id"],
            row["game_date"],
            row["season_type"],
            row["team_abbreviation_home"],
            row["team_name_home"],
            self.convert_points(row["pts_home"]),
            row["team_abbreviation_away"],
            row["team_name_away"],
            self.convert_points(row["pts_away"])
        )

        # Save the game using its ID.
        self.game_dict[game.game_id] = game

    def import_teams(self, filename):
        """Read team data from a CSV file and add it to team_dict."""

        # read the team CSV file.
        team_data = pd.read_csv(filename)

        # Create one TeamRecord object for every row
        team_data.apply(
            lambda row: self.add_team_from_row(row),
            axis=1
        )

    def add_team_from_row(self, row):
        """Create a TeamRecord from one row of the team DataFrame."""

        # Create a team object using the row data.
        team = TeamRecord(
            row["id"],
            row["full_name"],
            row["abbreviation"],
            row["nickname"],
            row["city"],
            row["state"],
            row["year_founded"]
        )

        # Save the team using its abbreviation.
        self.team_dict[team.abbreviation] = team

    def insert_game(self, game):
        """Insert a new game if the game ID is not already stored."""

        # Do not add duplicate games.
        if game.game_id in self.game_dict:
            return False

        # Add the game to the dictionary.
        self.game_dict[game.game_id] = game

        # Also save the game to the CSV file.
        self.save_game_to_csv(game, "game.csv")
        return True

    def delete_game(self, game_id):
        """Delete a game from the dictionary and CSV file."""

        # Game IDS are stored as strings.
        game_id = str(game_id)

        # Return False if the game does not exist.
        if game_id not in self.game_dict:
            return False

        # Remove the game from the dictionary
        del self.game_dict[game_id]

        # Read the original CSV
        game_data = pd.read_csv("game.csv")

        # Keep every row except the deleted game
        game_data = game_data[
            game_data["game_id"].astype(str) != game_id
        ]

        # Rewrite the CSV without the deleted game
        game_data.to_csv("game.csv", index=False)

        return True

    def search_game(self, game_id):
        """Search for and return a game using its game ID."""

        # Returns None if the game is not found
        return self.game_dict.get(str(game_id))

    def traverse_games(self, amount=10):
        """Return a list containing the first amount of stored games."""

        games = []

        # Add games until the requested amount is reached.
        for game in self.game_dict.values():
            games.append(game) # Add the game to the list

            # Stop adding games if the requested amount is reached.
            if len(games) == amount: 
                break

        # Return the list of games, which may be shorter than the requested amount.
        return games

    def search_by_team(self, abbreviation):
        """Return every game played by the selected team."""

        # Make the abbreviation uppercase for matching.
        abbreviation = abbreviation.upper()
        games = []

        # Check if the team was home or away in each game. 
        for game in self.game_dict.values():
            if (
                game.home_abbreviation == abbreviation
                or game.away_abbreviation == abbreviation
            ):
                games.append(game)

        return games

    def search_by_season(self, season_id):
        """Return every game from the selected season."""

        # Season IDs are stored as strings.
        season_id = str(season_id)
        games = []

        # Add games that match the season ID.
        for game in self.game_dict.values():
            if game.season_id == season_id:
                games.append(game)

        return games
    
    def team_summary(self, abbreviation):
        """Calculate and return a basic summary for one team."""

        # Make the abbreviation uppercase for matching.
        abbreviation = abbreviation.upper()

        # Initialize counters for the number of games, wins, and total points.
        games_played = 0
        wins = 0
        total_points = 0

        # Go through every game played by the selected team.
        for game in self.game_dict.values():
            # Check if the team was home or away and update the counters accordingly.
            if game.home_abbreviation == abbreviation:
                games_played += 1
                total_points += game.home_points

                # Count a win if the home team scored more points than the away team.
                if game.home_points > game.away_points:
                    wins += 1

            # Check if the team was the away team and update the counters accordingly.
            elif game.away_abbreviation == abbreviation:
                games_played += 1
                total_points += game.away_points

                # Count a win if the away team scored more points than the home team.
                if game.away_points > game.home_points:
                    wins += 1

        # No summary can be made if the team has no gmaes.
        if games_played == 0:
            return None

        # Get the full team name if team data is available.
        team = self.team_dict.get(abbreviation)

        if team:
            team_name = team.full_name
        else:
            team_name = abbreviation

        # Return the team's calculated statistics.
        return {
            "team_name": team_name,
            "games_played": games_played,
            "wins": wins,
            "losses": games_played - wins,
            "average_points": total_points / games_played
        }

    def convert_points(self, points):
        """Convert a points value to an integer."""

        # Use 0 if the score is missing.
        if pd.isna(points):
            return 0

        return int(points)

    def save_game_to_csv(self, game, filename):
        """
        Add one game record to the end of the CSV file.
        
        Parameters:
            game (GameRecord): Game object whose data should be saved.
            filename (str): CSV file that should receive the new row.

        The GameRecord attributes are first placed into a dictionary whose
        keys match the CSV column names. That dictionary becomes a one-row
        DataFrame, which pandas then appends to the existing file.

        Returns:
            None
        """

        new_row = {
            "game_id": game.game_id,
            "season_id": game.season_id,
            "game_date": game.game_date,
            "season_type": game.season_type,
            "team_abbreviation_home": game.home_abbreviation,
            "team_name_home": game.home_name,
            "pts_home": game.home_points,
            "team_abbreviation_away": game.away_abbreviation,
            "team_name_away": game.away_name,
            "pts_away": game.away_points
        }

        # pandas expects tabular data, so wrap the dictionary in a list to
        # create a DataFrame containing exactly one row.
        new_data = pd.DataFrame([new_row])

        # mode="a" appends instead of overwriting the file.
        # header=False prevents a second header row from being written.
        # index=False prevents pandas from adding an unwanted index column.
        new_data.to_csv(filename, mode="a", header=False, index=False)