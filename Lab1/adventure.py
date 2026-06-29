"""
Name: Tarun Ambati
Last updated: 06/22/2026
Description: A simple choose your own adventure game.
"""

def adventure():
    """ This function runs one session of a choose your own adventure.
        Arguments: None
        Returns: None (Printed text is not returned)
    """

    print()

    print("Welcome, worthy adventurer, to The Swamp,")
    print("home to Ally the Golden Gator and sourdough bread!")

    print()

    player_name, player_class = create_player()

    print()
    
    if player_class == "Warrior":
        health = 100
        mana = 50
        print("A brave warrior, ready to confront any challenge.")
    elif player_class == "Mage":
        health = 50
        mana = 100
        print("A cunning mage, capable of outwitting the strongest foe.")

    print()

    print("Here are your beginning stats:")
    print("Health: {}".format(health))
    print("Mana: {}".format(mana))

    print()

    print(player_name, "your quest is to rescue Ally from the Spartans")
    print("who hold her captive.")
    print("Let us begin...")

    print()

    # Add branches to the adventure here!

    print("Choose your path: [Left / Right]")
    print("Left: Battle and capture the dragon. (Faster, but more dangerous.)")
    print("Right: Sneak past the guards. (Slower, but safer.)")
    player_move1 = input("Which path do you choose? [Left / Right] ")
    if player_move1 == "Left":
        health = 25
        mana = 150
    elif player_move1 == "Right":
        health = 75
        mana = 75
    
    print("Stats:")
    print("Health: {}".format(health))
    print("Mana: {}".format(mana))

    print("Choose your next move: [Fight Castle / Sneak into Castle(underground tunnel)]")
    print("Fight Castle: Confront the Spartans head on. (Faster, but more dangerous.)")
    print("Sneak into Castle: Use the underground tunnel to bypass the guards). (Slower, but safer.)")
    player_move2 = input("Which path do you choose? [Fight Castle / Sneak into Castle] ")
    if player_move2 == "Fight Castle" and player_move1 == "Left":
        health = 1
        mana = 200
        print("You barely survive the battle, but your mana helps you defeat the Spartans.")
        print("You rescue Ally the Golden Gator. You win!")
        return 1

    elif player_move2 == "Fight Castle" and player_move1 == "Right":
        health = 0
        mana = 0
        print("You try to fight the Spartans, but you are too weak from sneaking around.")
        print("You are defeated. Game over.")
        return 0

    elif player_move2 == "Sneak into Castle" and player_move1 == "Left":
        health = 1
        mana = 100
        print("You sneak through the tunnel after battling the dragon.")
        print("You find Ally, but barely escape with your life. You win!")
        return 1

    elif player_move2 == "Sneak into Castle" and player_move1 == "Right":
        health = 0
        mana = 0
        print("You sneak into the tunnel, but the Spartans set a trap.")
        print("You are captured. Game over.")
        return 0

    print("Stats:")
    print("Health: {}".format(health))
    print("Mana: {}".format(mana))
    
    return 0


def create_player():
    """ Prompts the user for their name and class.
        Arguments: None
        Returns:
            - player_name (string): Name of the player
            - player_class (string): Class of the player
    """

    player_name = input("Before we begin, what should I call you? ")

    player_class = input("What is your specialty? [Warrior / Mage] ")
    while player_class != "Warrior" and player_class != "Mage":
        print("Invalid class. Please choose either 'Warrior' or 'Mage'.")
        player_class = input("What is your specialty? [Warrior / Mage] ")

    return player_name, player_class

win = 0
while win == 0:
    win = adventure()