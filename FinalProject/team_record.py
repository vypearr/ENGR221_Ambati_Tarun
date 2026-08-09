"""
Author: Alex Perez and Tarun Ambati
Last updated: August 2, 2026
Description: Defines the TeamRecord class used to store basic
information for one NBA team.
"""


class TeamRecord:
    """ 
    Store basic information about one NBA team.

    TeamRecord objects are used by the game manager so that a team can be
    looked up by its abbreviation and its full information can be accessed
    from one object.
    """
    def __init__(
        self,
        team_id,
        full_name,
        abbreviation,
        nickname,
        city,
        state,
        year_founded
    ):
        """
        Initialize a TeamRecord with the supplied team information.

        Parameters:
            team_id: Unique ID assigned to the team.
            full_name: Complete team name.
            abbreviation: Short team code, such as LAL or BOS.
            nickname: Team nickname.
            city: City associated with the team.
            state: State associated with the team.
            year_founded: Year the team/franchise was founded.

        All values are converted to strings. This keeps the stored values
        consistent even when data from a CSV is read as a number.
        """
        self.team_id = str(team_id)
        self.full_name = str(full_name)
        self.abbreviation = str(abbreviation)
        self.nickname = str(nickname)
        self.city = str(city)
        self.state = str(state)
        self.year_founded = str(year_founded)

    def __str__(self):
        """Return a formatted summary of the team.
            
        This special method is used automatically print() and str().
        Returns:
            str: The team name/abbreviation, location, and foundnig year.
        """
        # Combine the most useful team information into a display-friendly
        # string that can be shown directly in a terminal or user interface.
        return (
            f"{self.full_name} ({self.abbreviation})\n"
            f"City: {self.city}, {self.state}\n"
            f"Founded: {self.year_founded}"
        )
