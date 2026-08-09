"""
Author: Alex Perez and Tarun Ambati
Last updated: August 9, 2026
Description: Runs the Pygame user interface for the NBA Game
Records Manager.
"""

import os
import pygame

from game_record import GameRecord
from nba_game_manager import NBA_Game_Manager
from preferences import Preferences


class TextBox:
    # Represents one editable text field in the Pygame window.
    def __init__(self, x, y, width, height, label):
        # The rectangle stores the position and size of the text box.
        self.rect = pygame.Rect(x, y, width, height)

        # Text shown above the input field.
        self.label = label

        # Stores what the user types.
        self.text = ""

        # True when the user has clicked inside this text box.
        self.active = False

    def handle_event(self, event):
        """Update the text box from a mouse or keyboard event."""

        # Check whether the mouse was clicked inside this text box.
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

        # Only accept keyboard input while this text box is active.
        if event.type == pygame.KEYDOWN and self.active:
            # Remove the last typed character when Backspace is pressed.
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            # Pressing Enter finishes typing in this box.
            elif event.key == pygame.K_RETURN:
                self.active = False
            # Add typed characters while keeping the input reasonably short.
            elif len(self.text) < 35:
                self.text += event.unicode

    def draw(self, screen):
        """Draw the label and text box."""

        # Render the label as a Pygame surface.
        label = Preferences.SMALL_FONT.render(
            self.label,
            True,
            Preferences.SECONDARY_TEXT_COLOR
        )
        screen.blit(label, (self.rect.x, self.rect.y - 20))

        # Change the text box color when it is selected.
        if self.active:
            color = Preferences.INPUT_ACTIVE_COLOR
        else:
            color = Preferences.INPUT_COLOR

        # Draw the text box background.
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(
            screen,
            Preferences.BORDER_COLOR,
            self.rect,
            2
        )

        # Render whatever the user typed inside the box.
        text = Preferences.LABEL_FONT.render(
            self.text,
            True,
            Preferences.TEXT_COLOR
        )
        screen.blit(text, (self.rect.x + 8, self.rect.y + 8))


class Button:
    # Represents one clickable button in the UI.
    def __init__(self, x, y, width, height, text, action):
        # Rectangle used for drawing and collision detection.
        self.rect = pygame.Rect(x, y, width, height)

        # Text displayed on the button.
        self.text = text

        # Name of the action that should run when the button is clicked.
        self.action = action

    def draw(self, screen):
        """Draw the button."""

        # Use a different color when the mouse is hovering over the button.
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            color = Preferences.BUTTON_HOVER_COLOR
        else:
            color = Preferences.BUTTON_COLOR

        # Draw the visible rounded button.
        pygame.draw.rect(screen, color, self.rect, border_radius=6)

        label = Preferences.LABEL_FONT.render(
            self.text,
            True,
            Preferences.BUTTON_TEXT_COLOR
        )
        # Center the button text, then place it on the screen.
        label_rect = label.get_rect(center=self.rect.center)
        screen.blit(label, label_rect)


class Controller:
    def __init__(self):
        # Initialize all Pygame modules before creating fonts or windows.
        pygame.init()

        # Create the fonts after Pygame has been initialized.
        Preferences.TITLE_FONT = pygame.font.Font(None, 42)
        Preferences.HEADING_FONT = pygame.font.Font(None, 30)
        Preferences.LABEL_FONT = pygame.font.Font(None, 24)
        Preferences.SMALL_FONT = pygame.font.Font(None, 20)

        # Create the main program window.
        self.screen = pygame.display.set_mode(
            (Preferences.SCREEN_WIDTH, Preferences.SCREEN_HEIGHT)
        )
        pygame.display.set_caption("NBA Game Records Manager")

        # Clock controls how quickly the Pygame loop runs.
        self.clock = pygame.time.Clock()

        # Manager object handles the game/team data and hash table operations.
        self.manager = NBA_Game_Manager()

        # Switch the draw/event logic back to the main page.
        self.page = "main"
        self.message = "Enter a game ID or team abbreviation."
        self.message_color = Preferences.TEXT_COLOR
        self.output_lines = []

        # Main text field used for game IDs and team abbreviations.
        self.main_input = TextBox(
            55,
            145,
            330,
            45,
            "Game ID or team abbreviation"
        )

        # Buttons displayed on the main page.
        # Each button stores an action name used by perform_action().
        self.main_buttons = [
            Button(55, 225, 190, 45, "Search Game", "search_game"),
            Button(260, 225, 190, 45, "Delete Game", "delete_game"),
            Button(55, 285, 190, 45, "Search Team", "search_team"),
            Button(260, 285, 190, 45, "Team Summary", "team_summary"),
            Button(55, 345, 190, 45, "Display Games", "display_games"),
            Button(260, 345, 190, 45, "Insert Game", "insert_page")
        ]

        # Input fields used when adding a new game.
        self.insert_boxes = [
            TextBox(55, 140, 220, 40, "Game ID"),
            TextBox(295, 140, 220, 40, "Season ID"),
            TextBox(535, 140, 220, 40, "Game date"),
            TextBox(775, 140, 220, 40, "Season type"),
            TextBox(55, 225, 220, 40, "Home abbreviation"),
            TextBox(295, 225, 220, 40, "Home team name"),
            TextBox(535, 225, 220, 40, "Home points"),
            TextBox(55, 310, 220, 40, "Away abbreviation"),
            TextBox(295, 310, 220, 40, "Away team name"),
            TextBox(535, 310, 220, 40, "Away points")
        ]

        # Buttons shown on the insert-game page.
        self.insert_buttons = [
            Button(55, 395, 190, 45, "Add Game", "add_game"),
            Button(260, 395, 190, 45, "Back", "main_page")
        ]

    def load_data(self):
        """Load the CSV files after checking that they exist."""

        # Make sure the required dataset files are available first.
        if not os.path.exists("game.csv"):
            self.set_message("game.csv was not found.", True)
            return False

        if not os.path.exists("team.csv"):
            self.set_message("team.csv was not found.", True)
            return False

        # Load the CSV data into the manager's dictionaries.
        self.manager.import_games("game.csv")
        self.manager.import_teams("team.csv")

        self.set_message(
            f"Loaded {len(self.manager.game_dict)} games and "
            f"{len(self.manager.team_dict)} teams."
        )
        return True

    def set_message(self, message, error=False):
        """Set the status message displayed on the screen."""

        # Store the text that appears at the bottom of the window.
        self.message = message

        if error:
            self.message_color = Preferences.ERROR_COLOR
        else:
            self.message_color = Preferences.SUCCESS_COLOR

    def wrap_text(self, text, max_characters=72):
        """Split text into lines that fit inside the output panel."""

        # This list stores each output line after wrapping.
        lines = []

        # Keep existing line breaks, then split long lines into words.
        for original_line in text.split("\n"):
            words = original_line.split()
            line = ""

            # Build one output line word by word.
            for word in words:
                test_line = line + word + " "

                # Start a new line if the current one gets too long.
                if len(test_line) > max_characters:
                    lines.append(line.strip())
                    line = word + " "
                else:
                    line = test_line

            lines.append(line.strip())

        return lines

    def search_game(self):
        """Search for a game using the text in the main input box."""

        # Read the game ID from the main text box.
        game_id = self.main_input.text.strip()

        if game_id == "":
            self.set_message("Enter a game ID first.", True)
            return

        # Ask the manager to perform the dictionary/hash-table lookup.
        game = self.manager.search_game(game_id)

        if game is None:
            self.output_lines = []
            self.set_message("Game not found.", True)
        else:
            # Convert the GameRecord to text and prepare it for display.
            self.output_lines = self.wrap_text(str(game))
            self.set_message("Game found.")

    def delete_game(self):
        """Delete a game using the text in the main input box."""

        # Read the game ID from the main text box.
        game_id = self.main_input.text.strip()

        if game_id == "":
            self.set_message("Enter a game ID first.", True)
            return

        if self.manager.delete_game(game_id):
            self.output_lines = []
            self.main_input.text = ""
            self.set_message("Game deleted.")
        else:
            self.set_message("Game not found.", True)

    def search_team(self):
        """Display games played by one team."""

        # Team abbreviations are converted to uppercase for consistency.
        abbreviation = self.main_input.text.strip().upper()

        if abbreviation == "":
            self.set_message("Enter a team abbreviation first.", True)
            return

        # Search every game record for the selected team.
        games = self.manager.search_by_team(abbreviation)

        if len(games) == 0:
            self.output_lines = []
            self.set_message("No games were found.", True)
            return

        self.output_lines = [f"First 3 of {len(games)} matching games:"]
        self.output_lines.append("")

        # Only add the first few matches so the output panel is not overloaded.
        for game in games[:5]:
            self.output_lines.extend(self.wrap_text(str(game)))
            self.output_lines.append("")

        self.set_message("Team games found.")

    def team_summary(self):
        """Display a calculated summary for one team."""

        # Team abbreviations are converted to uppercase for consistency.
        abbreviation = self.main_input.text.strip().upper()

        if abbreviation == "":
            self.set_message("Enter a team abbreviation first.", True)
            return

        # Ask the manager to calculate wins, losses, and average points.
        summary = self.manager.team_summary(abbreviation)

        if summary is None:
            self.output_lines = []
            self.set_message("No games were found for that team.", True)
            return

        self.output_lines = [
            f"Team: {summary['team_name']}",
            f"Games played: {summary['games_played']}",
            f"Wins: {summary['wins']}",
            f"Losses: {summary['losses']}",
            f"Average points: {summary['average_points']:.2f}"
        ]
        self.set_message("Team summary created.")

    def display_games(self):
        """Traverse and display the first five games."""

        # Traverse the dictionary and return the first three stored games.
        games = self.manager.traverse_games(3)
        self.output_lines = []

        for game in games[:3]:
            self.output_lines.extend(self.wrap_text(str(game)))
            self.output_lines.append("")

        self.set_message(f"Displaying {len(games)} games.")

    def open_insert_page(self):
        """Open the insert-game form."""

        # Switch the draw/event logic to the insert form.
        self.page = "insert"
        self.output_lines = []
        self.set_message("Fill in each field to add a game.")

    def open_main_page(self):
        """Return to the main page."""

        # Switch the draw/event logic back to the main page.
        self.page = "main"
        self.set_message("Enter a game ID or team abbreviation.")

    def add_game(self):
        """Create and insert a game from the insert form."""

        # Collect the text from every input box in order.
        values = []

        # Draw every input field on the insert page.
        for box in self.insert_boxes:
            values.append(box.text.strip())

        # Do not allow insertion if any field was left empty.
        for value in values:
            if value == "":
                self.set_message("Complete every field.", True)
                return

        home_points = values[6]
        away_points = values[9]

        # Check that both point values contain only whole-number digits.
        if not home_points.isdigit() or not away_points.isdigit():
            self.set_message("Points must be whole numbers.", True)
            return

        # Create a new GameRecord object from the form values.
        game = GameRecord(
            values[0],
            values[1],
            values[2],
            values[3],
            values[4].upper(),
            values[5],
            int(home_points),
            values[7].upper(),
            values[8],
            int(away_points)
        )

        # Insert the new record through NBA_Game_Manager.
        if self.manager.insert_game(game):
            # Clear the form after a successful insertion.
            # Draw every input field on the insert page.
            for box in self.insert_boxes:
                box.text = ""

            self.set_message("Game inserted.")
        else:
            self.set_message("That game ID already exists.", True)

    def perform_action(self, action):
        """Run the method connected to a clicked button."""

        # Match the button's stored action string to the correct method.
        if action == "search_game":
            self.search_game()

        elif action == "delete_game":
            self.delete_game()

        elif action == "search_team":
            self.search_team()

        elif action == "team_summary":
            self.team_summary()

        elif action == "display_games":
            self.display_games()

        elif action == "insert_page":
            self.open_insert_page()

        elif action == "add_game":
            self.add_game()

        elif action == "main_page":
            self.open_main_page()

    def handle_events(self):
        """Handle mouse and keyboard events."""

        # Read all mouse, keyboard, and window events from Pygame.
        for event in pygame.event.get():
            # Stop the main loop when the user closes the window.
            if event.type == pygame.QUIT:
                return False

            # Send events only to controls on the page currently being shown.
            if self.page == "main":
                self.main_input.handle_event(event)
                buttons = self.main_buttons

            else:
                # Clear the form after a successful insertion.
            # Draw every input field on the insert page.
                for box in self.insert_boxes:
                    box.handle_event(event)

                buttons = self.insert_buttons

            # When the mouse is clicked, check every visible button.
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    # collidepoint() checks whether the click was inside the button.
                    if button.rect.collidepoint(event.pos):
                        self.perform_action(button.action)

        return True

    def draw_header(self, subtitle):
        """Draw the title and subtitle."""

        # Render and draw the main title.
        title = Preferences.TITLE_FONT.render(
            "NBA Game Records Manager",
            True,
            Preferences.TITLE_COLOR
        )
        self.screen.blit(title, (55, 35))

        subtitle_label = Preferences.LABEL_FONT.render(
            subtitle,
            True,
            Preferences.SECONDARY_TEXT_COLOR
        )
        self.screen.blit(subtitle_label, (57, 82))

    def draw_main_page(self):
        """Draw the main search and operation page."""

        self.draw_header(
            "Search, insert, delete, and traverse NBA game records."
        )

        # Draw the white panel that contains the main input and buttons.
        pygame.draw.rect(
            self.screen,
            Preferences.PANEL_COLOR,
            pygame.Rect(35, 115, 435, 320),
            border_radius=8
        )

        self.main_input.draw(self.screen)

        # Draw every button on the main page.
        for button in self.main_buttons:
            button.draw(self.screen)

        self.draw_output_panel()

    def draw_insert_page(self):
        """Draw the insert-game page."""

        self.draw_header("Enter the information for a new NBA game.")

        # Draw the large panel that holds the insert-game form.
        pygame.draw.rect(
            self.screen,
            Preferences.PANEL_COLOR,
            pygame.Rect(35, 110, 1015, 355),
            border_radius=8
        )

        # Draw every input field on the insert page.
        for box in self.insert_boxes:
            box.draw(self.screen)

        for button in self.insert_buttons:
            button.draw(self.screen)

        note = Preferences.SMALL_FONT.render(
            "Close program to save changes to game.csv.",
            True,
            Preferences.SECONDARY_TEXT_COLOR
        )
        self.screen.blit(note, (55, 485))

    def draw_output_panel(self):
        """Draw the output area on the main page."""

        # Define the position and size of the output panel.
        panel = pygame.Rect(500, 115, 550, 500)

        # Draw the white output panel on the right side.
        pygame.draw.rect(
            self.screen,
            Preferences.PANEL_COLOR,
            panel,
            border_radius=8
        )

        heading = Preferences.HEADING_FONT.render(
            "Output",
            True,
            Preferences.TITLE_COLOR
        )
        self.screen.blit(heading, (525, 140))

        # Starting vertical position for the first output line.
        y = 185

        # Draw one output line at a time, up to what fits in the panel.
        for line in self.output_lines[:19]:
            # Render the label as a Pygame surface.
            label = Preferences.SMALL_FONT.render(
                line,
                True,
                Preferences.TEXT_COLOR
            )
            # blit() places the rendered text surface onto the main screen.
            self.screen.blit(label, (525, y))

            # Move the next line lower so the lines do not overlap.
            y += 22

    def draw_status(self):
        """Draw the current status message."""

        # Render the status/error message shown at the bottom.
        status = Preferences.SMALL_FONT.render(
            self.message,
            True,
            self.message_color
        )
        self.screen.blit(status, (55, 650))

    def draw(self):
        """Draw the current program page."""

        # Clear the previous frame by repainting the background.
        self.screen.fill(Preferences.BACKGROUND_COLOR)

        if self.page == "main":
            self.draw_main_page()
        else:
            self.draw_insert_page()

        self.draw_status()
        # Update the visible window after all drawing is finished.
        pygame.display.flip()

    def run(self):
        """Load the data and run the user interface."""

        # Load the dataset before starting the Pygame event loop.
        self.load_data()
        running = True

        # Main Pygame loop: handle input, redraw, and repeat.
        while running:
            running = self.handle_events()
            self.draw()
            # Limit the loop to about 60 frames per second.
            self.clock.tick(60)

        pygame.quit()


# Start the program only when this file is run directly.
if __name__ == "__main__":
    controller = Controller()
    controller.run()
