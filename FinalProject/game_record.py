"""
Author: Alex Perez and Tarun Ambati
Last updated: August 9, 2026
Description: Defines the GameRecord class used to store information
for one NBA game.

This module contains the data class-like object for representing one NBA game.
A GameRecord stores identifying information about the game, season information,
and the names, abbreviations, and scores of both teams.
"""


class GameRecord:
    """
    Store all important information for one NBA game.

    Each GameRecord object represents a single game. The object keeps the data
    together so that other parts of the proogram can easily search, display,
    summarize, or save a game without passing many seperate variables around.
    """
    def __init__(
        self,
        game_id,
        season_id,
        game_date,
        season_type,
        home_abbreviation,
        home_name,
        home_points,
        away_abbreviation,
        away_name,
        away_points
    ):
        """ Initialize a new GameRecord object.
        Parameters:
            game_id (str): Unique identifier for the game.
            season_id (str): Identifier for the season.
            game_date (str): Date of the game in YYYY-MM-DD format.
            season_type (str): Type of the season (e.g., Regular, Playoffs).
            home_abbreviation (str): Abbreviation for the home team.
            home_name (str): Full name of the home team.
            home_points (int): Points scored by the home team.
            away_abbreviation (str): Abbreviation for the away team.
            away_name (str): Full name of the away team.
            away_points (int): Points scored by the away team.
        
        The values are convertes to consisten types before being stored.
        IDs and text values are saved as strings, while scores are integers.
        This makes later comparisons and calculations more predictable.
        """
        
        self.game_id = str(game_id)
        self.season_id = str(season_id)
        self.game_date = str(game_date)
        self.season_type = str(season_type)

        self.home_abbreviation = str(home_abbreviation)
        self.home_name = str(home_name)
        self.home_points = int(home_points)

        self.away_abbreviation = str(away_abbreviation)
        self.away_name = str(away_name)
        self.away_points = int(away_points)

    def __str__(self):
        """
        Return a readeble, multi-line summary of the game.

        This special method is automatically used when a Gamerecord is passed
        to str() or printe(). The returned text includes the game
        ID, date, season information, both teams, and the final score.

        Returns:
            str: A formatted description of the game.
         """

        # Build one formatted string across several lines. Slicing [:10]
        # removes any time information that may follow the date in the game_date.
        return (
            f"Game ID: {self.game_id}\n"
            f"Date: {self.game_date[:10]}\n"
            f"Season: {self.season_id} - {self.season_type}\n"
            f"{self.away_name} ({self.away_abbreviation}) "
            f"{self.away_points} - {self.home_points} "
            f"{self.home_name} ({self.home_abbreviation})"
        )
