"""
Author: Alex Perez and Tarun Ambati
Last updated: August 9, 2026
Description: Stores the display settings used by the NBA Game
Records Manager user interface.
"""

import pygame


class Preferences:
    """ 
        Store shared visual settings for the NBA game Records Manager interface.
        
        The values below are class attributes ratehr than instance attributes.
        This means other files can access them directly with expressions such as
        Preferences.SCREEN_WIDTH or Preferences.BUTTON_COLOR without creating a 
        Preferences object first.
        """
    SCREEN_WIDTH = 1100
    SCREEN_HEIGHT = 700

    BACKGROUND_COLOR = (238, 242, 247)
    PANEL_COLOR = (255, 255, 255)
    TITLE_COLOR = (30, 55, 90)
    TEXT_COLOR = (30, 30, 30)
    SECONDARY_TEXT_COLOR = (90, 98, 110)

    BUTTON_COLOR = (37, 99, 235)
    BUTTON_HOVER_COLOR = (29, 78, 216)
    BUTTON_TEXT_COLOR = (255, 255, 255)

    INPUT_COLOR = (255, 255, 255)
    INPUT_ACTIVE_COLOR = (219, 234, 254)
    BORDER_COLOR = (170, 178, 190)

    SUCCESS_COLOR = (22, 130, 75)
    ERROR_COLOR = (190, 45, 45)

    TITLE_FONT = None
    HEADING_FONT = None
    LABEL_FONT = None
    SMALL_FONT = None
