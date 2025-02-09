"""CSC111 Project 1: Text Adventure Game - Simulator

Instructions (READ THIS FIRST!)
===============================

This Python module contains code for Project 1 that allows a user to simulate an entire
playthrough of the game. Please consult the project handout for instructions and details.

You can copy/paste your code from the ex1_simulation file into this one, and modify it as needed
to work with your game.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""
from __future__ import annotations
from proj1_event_logger import Event, EventList
from adventure import AdventureGame
from game_entities import Location


class AdventureGameSimulation:
    """A simulation of an adventure game playthrough.
    """
    # Private Instance Attributes:
    #   - _game: The AdventureGame instance that this simulation uses.
    #   - _events: A collection of the events to process during the simulation.
    _game: AdventureGame
    _events: EventList

    def __init__(self, game_data_file: str, initial_location_id: int, commands: list[str]) -> None:
        """Initialize a new game simulation based on the given game data, that runs through the given commands.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands at each associated location in the game
        """
        self._events = EventList()
        self._game = AdventureGame(game_data_file, initial_location_id)

        current_location = self._game.get_location()
        # 判断是否为首次访问，如果是则使用长描述，否则使用简要描述
        if not current_location.visited:
            description = current_location.long_description
            current_location.visited = True
        else:
            description = current_location.brief_description

        first_event = Event(id_num=current_location.id_num,
                            description=description,
                            next_command=None)
        self._events.add_event(first_event)

        self.generate_events(commands, current_location)

    def generate_events(self, commands: list[str], current_location: Location) -> None:
        """Generate all events in this simulation.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands at each associated location in the game
        """

        for command in commands:
            if command in current_location.available_commands:
                next_location_id = current_location.available_commands[command]
                next_location = self._game.get_location(next_location_id)
                # 根据是否首次访问选择使用长描述或简要描述
                if not next_location.visited:
                    description = next_location.long_description
                    next_location.visited = True
                else:
                    description = next_location.brief_description
                new_event = Event(id_num=next_location.id_num,
                                  description=description,
                                  next_command=command)
                self._events.add_event(new_event, command)
                current_location = next_location

    def get_id_log(self) -> list[int]:
        """
        Get back a list of all location IDs in the order that they are visited within a game simulation
        that follows the given commands.

        >>> sim = AdventureGameSimulation('sample_locations.json', 1, ["go east"])
        >>> sim.get_id_log()
        [1, 2]

        >>> sim = AdventureGameSimulation('sample_locations.json', 1, ["go east", "go east", "buy coffee"])
        >>> sim.get_id_log()
        [1, 2, 3, 3]
        """

        # Note: We have completed this method for you. Do NOT modify it for ex1.

        return self._events.get_id_log()

    def run(self) -> None:
        """Run the game simulation and log location descriptions."""

        # Note: We have completed this method for you. Do NOT modify it for ex1.

        current_event = self._events.first  # Start from the first event in the list

        while current_event:
            print(current_event.description)
            if current_event is not self._events.last:
                print("You choose:", current_event.next_command)

            # Move to the next event in the linked list
            current_event = current_event.next


if __name__ == "__main__":
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })

    # Define walkthroughs
    win_walkthrough = ["go east", "go north"]  # Example commands to win
    lose_demo = ["go west", "go south"]  # Example commands to lose
    inventory_demo = ["go east", "pick up key", "inventory"]  # Example for inventory feature

    # Run win walkthrough
    win_sim = AdventureGameSimulation('sample_locations.json', 1, win_walkthrough)
    assert win_sim.get_id_log() == [1, 2, 3]
    win_sim.run()

    # Run lose demo
    lose_sim = AdventureGameSimulation('sample_locations.json', 1, lose_demo)
    assert lose_sim.get_id_log() == [1, 4, 5]
    lose_sim.run()

    # Run inventory demo
    inventory_sim = AdventureGameSimulation('sample_locations.json', 1, inventory_demo)
    assert inventory_sim.get_id_log() == [1, 2]
    inventory_sim.run()
