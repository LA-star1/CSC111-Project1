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

    # TODO: Copy/paste your code from ex1_simulation below, and make adjustments as needed
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

        # TODO: Complete this method as specified. For each command, generate the event and add
        #  it to self._events.
        # Hint: current_location.available_commands[command] will return the next location ID
        # which executing <command> while in <current_location_id> leads to
        # for command in commands:
        #     if command in current_location.available_commands:
        #         next_location_id = current_location.available_commands[command]
        #         next_location = self._game.get_location(next_location_id)
        #         new_event = Event(id_num=next_location.id_num, description=next_location.long_description, next_command=command)
        #         self._events.add_event(new_event, command)
        #         current_location = next_location
        #     elif command == "pick up" or command == "unlock" or "12345678" or "csc is the best!" or "drop":
        #         cur_location_id = current_location.id_num
        #         next_location = self._game.get_location(cur_location_id)
        #         new_event = Event(id_num=next_location.id_num, description=next_location.brief_description,
        #                           next_command=command)
        #         self._events.add_event(new_event, command)
        #         current_location = next_location
        #     elif command == "red bull" or "computer drophy":
        #         pass

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
            elif command == "pick up":
                new_event = Event(id_num=current_location.id_num, description=current_location.brief_description,
                                  next_command=command)
                self._events.add_event(new_event, command)
            elif command == "unlock":
                new_event = Event(id_num=current_location.id_num, description=current_location.brief_description,
                                  next_command=command)
                self._events.add_event(new_event, command)
            elif command == "drop":
                new_event = Event(id_num=current_location.id_num, description=current_location.brief_description,
                                  next_command=command)
                self._events.add_event(new_event, command)

    def get_id_log(self) -> list[int]:
        """
        Get back a list of all location IDs in the order that they are visited within a game simulation
        that follows the given commands.


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

    # TODO: Modify the code below to provide a walkthrough of commands needed to win and lose the game
    win_walkthrough = ["pick up",
                       "go west",
                       "go west",
                       "go down",
                       "go north",
                       "go west",
                       "pick up",
                       "go east",
                       "go north",
                       "go north",
                       "go west",
                       "go west",
                       "go west",
                       "go up",
                       "go west",
                       "go south",
                       "go north",
                       "go east",
                       "go down",
                       "go east",
                       "go north",
                       "pick up",
                       "go south",
                       "go east",
                       "go east",
                       "go north",
                       "go north",
                       "go west",
                       "go east",
                       "go north",
                       "go up",
                       "go south",
                       "go west",
                       "pick up",
                       "go east",
                       "go east",
                       "pick up",
                       "go west",
                       "go north",
                       "go up",
                       "go south",
                       "go south",
                       "unlock",
                       "12345678"
                       "pick up",
                       "go north",
                       "go north",
                       "go down",
                       "go down",
                       "go south",
                       "go south",
                       "go south",
                       "go west",
                       "go west",
                       "go west",
                       "go up",
                       "go west",
                       "go south",
                       "drop",
                       "red bull",
                       "drop",
                       "computer award",
                       "go west",
                       "unlock",
                       "csc is the best!"
                       "pick up",
                       "go east",
                       "go north",
                       "go east",
                       "go down",
                       "go east",
                       "go east",
                       "go east",
                       "go south",
                       "go south",
                       "go south",
                       "go up",
                       "go east",
                       "go east"]  # Create a list of all the commands needed to walk through your game to win it
    expected_log1 = [
        1203,  # Your Dorm
        1203,
        1202,  # Hallway
        1201,  # Elevator (Second Floor)
        1102,  # Elevator (First Floor)
        1101,  # Lobby
        1103,  # Front Desk
        1103,  # Picked up t-card (no location change)
        1101,  # Lobby
        1,  # Residence
        2,  # Queens Park
        4,  # Bahen Centre for Information Technology
        4101,  # Bahen First Floor Hallway
        4103,  # Bahen First Floor Stairway
        4201,  # Bahen Second Floor Stairway
        4205,  # Bahen Second Floor Hallway
        4202,  # Bahen Study Circle
        4205,  # Bahen Second Floor Hallway
        4201,  # Bahen Second Floor Stairway
        4103,  # Bahen First Floor Stairway
        4101,  # Bahen First Floor Hallway
        4102,  # CS Competition Awards Room
        4102,  # Picked up computer award (no location change)
        4101,  # Bahen First Floor Hallway
        4,  # Bahen Centre
        2,  # Queens Park
        3,  # Robarts Library
        3101,  # Robarts Lobby
        3103,  # Robarts Common
        3101,  # Robarts Lobby
        3104,  # First Floor Elevator
        3204,  # Second Floor Elevator
        3201,  # Second Floor Hallway
        3202,  # Cafeteria
        3202,  # Picked up red bull (no location change)
        3201,  # Second Floor Hallway
        3203,  # Study Lounge
        3203,  # Picked up laptop charger (no location change)
        3201,  # Second Floor Hallway
        3204,  # Second Floor Elevator
        3905,  # Ninth Floor Elevator
        3901,  # Ninth Floor Hallway
        3902,  # Study Rooms
        3902,  # Unlocked safe (no location change)
        3902,  # Picked up laptop (no location change)
        3901,  # Ninth Floor Hallway
        3905,  # Ninth Floor Elevator
        3204,  # Second Floor Elevator
        3104,  # First Floor Elevator
        3101,  # Robarts Lobby
        3,  # Robarts Library
        2,  # Queens Park
        4,  # Bahen Centre
        4101,  # Bahen First Floor Hallway
        4103,  # Bahen First Floor Stairway
        4201,  # Bahen Second Floor Stairway
        4205,  # Bahen Second Floor Hallway
        4202,  # Bahen Study Circle
        4202,  # Dropped red bull (no location change)
        4202,  # Dropped computer award (no location change),
        4206,  # Bahen Computer Lab
        4206,  # Unlocked safe (no location change)
        4206,  # Picked up usb drive (no location change)
        4202,  # Bahen Study Circle
        4205,  # Bahen Second Floor Hallway
        4201,  # Bahen Second Floor Stairway
        4103,  # Bahen First Floor Stairway
        4101,  # Bahen First Floor Hallway
        4,  # Bahen Centre
        2,  # Queens Park
        1,  # Residence
        1101,  # Your Dorm
        1102,
        1201,  # Elevator (Second Floor)
        1202,  # Hallway
        1203  # Your Dorm
    ]  # Update this log list to include the IDs of all locations that would be visited
    # Uncomment the line below to test your walkthrough
    sim = AdventureGameSimulation('game_data.json', 1203, win_walkthrough)
    assert expected_log1 == sim.get_id_log()

    # Create a list of all the commands needed to walk through your game to reach a 'game over' state
    # lose_demo = ["go west",
    #              "go east",
    #              "go west",
    #              "go east",
    #              "go west",
    #              "go east",
    #              "go west",
    #              "go east",
    #              "go west",
    #              "go east",
    #              "go west",
    #              "go east",
    #              "go west",
    #              "go east",
    #              "go west",
    #              "go east",
    #              "go west",
    #              "go east",
    #              "go west",
    #              "go east",
    #              "go west",
    #              "go east",
    #              "go west",
    #              "go east",
    #              "go west",
    #              "go east",
    #              "go west",
    #              "go east",
    #              "go west",
    #              "go east",
    #              "go west",
    #              "go east",
    #              "go west",
    #              "go east",
    #              "go west",
    #              "go east",
    #              "go west",
    #              "go east",
    #              "go west",
    #              "go east",
    #              "go west",
    #              "go east",
    #              "go west",
    #              "go east",
    #              "go west",
    #              "go east",
    #              "go west",
    #              "go east",
    #              "go west",
    #              "go east",
    #              "go west",
    #              "go east",
    #              "go west",
    #              "go east",
    #              "go west",
    #              "go east",
    #              "go west",
    #              "go east",
    #              "go west",
    #              "go east",
    #              "go west",
    #              "go east",
    #              "go west",
    #              "go east",
    #              "go west",
    #              "go east",
    #              "go west",
    #              "go east",
    #              "go west",
    #              "go east",
    #              ]
    # expected_log2 = [1203, 1202,
    #                  1203, 1202,
    #                  1203, 1202,
    #                  1203, 1202,
    #                  1203, 1202,
    #                  1203, 1202,
    #                  1203, 1202,
    #                  1203, 1202,
    #                  1203, 1202,
    #                  1203, 1202,
    #                  1203, 1202,
    #                  1203, 1202,
    #                  1203, 1202,
    #                  1203, 1202,
    #                  1203, 1202,
    #                  1203, 1202,
    #                  1203, 1202,
    #                  1203, 1202,
    #                  1203, 1202,
    #                  1203, 1202,
    #                  1203, 1202,
    #                  1203, 1202,
    #                  1203, 1202,
    #                  1203, 1202,
    #                  1203, 1202,
    #                  1203, 1202,
    #                  1203, 1202,
    #                  1203, 1202,
    #                  1203, 1202,
    #                  1203, 1202,
    #                  1203, 1202,
    #                  1203, 1202,
    #                  1203, 1202,
    #                  1203, 1202,
    #                  1203, 1202,
    #                  1203
    #                  ]  # Update this log list to include the IDs of all locations that would be visited
    # # Uncomment the line below to test your demo
    # sim = AdventureGameSimulation('game_data.json', 1203, lose_demo)
    # assert expected_log2 == sim.get_id_log()

    # TODO: Add code below to provide walkthroughs that show off certain features of the game
    # TODO: Create a list of commands involving visiting locations, picking up items, and then
    #   checking the inventory, your list must include the "inventory" command at least once
    # inventory_demo = [..., "inventory", ...]
    # expected_log = []
    # assert expected_log == AdventureGameSimulation(...)

    # scores_demo = [..., "score", ...]
    # expected_log = []
    # assert expected_log == AdventureGameSimulation(...)

    # Add more enhancement_demos if you have more enhancements
    # enhancement1_demo = [...]
    # expected_log = []
    # assert expected_log == AdventureGameSimulation(...)

    # Note: You can add more code below for your own testing purposes
