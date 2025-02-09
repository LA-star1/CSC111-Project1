"""CSC111 Project 1: Text Adventure Game - Game Entities

Instructions (READ THIS FIRST!)
===============================

This Python module contains the entity classes for Project 1, to be imported and used by
 the `adventure` module.
 Please consult the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""
from dataclasses import dataclass


@dataclass
class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - id_num: The unique ID for the location.
        - name: The name of the location.
        - brief_description: A short description of the location.
        - available_commands: A dictionary mapping directions (e.g., "north", "south") to location IDs.
        - items: A list of items currently present in the location.
        - visited: Whether this location has been visited by the player.

    Representation Invariants:
        - id_num > 0
        - name is a non-empty string
        - brief_description and long_description are non-empty strings
        - available_commands.keys() contain only valid directions: "north", "south", "east", "west"

    """
    id_num: int
    _name: str
    brief_description: str
    long_description: str
    available_commands: dict
    items: list
    visited: bool

    # This is just a suggested starter class for Location.
    # You may change/add parameters and the data available for each Location object as you see fit.
    #
    # The only thing you must NOT change is the name of this class: Location.
    # All locations in your game MUST be represented as an instance of this class.

    def __init__(self, strl: list, available_commands: dict, items: list) -> None:
        """Initialize a new location.

        # TODO Add more details here about the initialization if needed
        """

        self.id_num = strl[0]
        self._name = strl[1]
        self.brief_description = strl[2]
        self.long_description = strl[3]
        self.available_commands = available_commands
        self.items = items
        self.visited = False

    def get_name(self) -> str:
        """return name"""
        return self._name


@dataclass
class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - name: The name of the item.
        - description: A brief description of the item.
        - start_position: The ID of the location where the item starts.
        - target_position: The ID of the location where the item should be deposited.
        - target_points: The number of points earned when the item is deposited correctly.

    Representation Invariants:
        - start_position > 0
        - target_position > 0
        - target_points >= 0
    """

    # NOTES:
    # This is just a suggested starter class for Item.
    # You may change these parameters and the data available for each Item object as you see fit.
    # (The current parameters correspond to the example in the handout).
    #
    # The only thing you must NOT change is the name of this class: Item.
    # All item objects in your game MUST be represented as an instance of this class.

    name: str
    description: str
    start_position: int
    target_position: int
    target_points: int


# Note: Other entities you may want to add, depending on your game plan:
# - Puzzle class to represent special locations (could inherit from Location class if it seems suitable)
# - Player class
# etc.

if __name__ == "__main__":
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })
