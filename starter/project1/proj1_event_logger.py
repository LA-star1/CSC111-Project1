"""CSC111 Project 1: Text Adventure Game - Event Logger

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

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
from dataclasses import dataclass
from typing import Optional


@dataclass
class Event:
    """
    A node representing one event in an adventure game.

    Instance Attributes:
      - id_num: Integer id of this event's location
      - description: Long description of this event's location
      - next_command: String command which leads this event to the next event, None if this is the last game event
      - next: Event object representing the next event in the game, or None if this is the last game event
      - prev: Event object representing the previous event in the game, None if this is the first game event
    """

    id_num: int
    description: str
    next_command: Optional[str] = None
    next: Optional[Event] = None
    prev: Optional[Event] = None


class EventList:
    """
    A linked list of game events.

    Instance Attributes:
        - first: Event object representing the first event in the linked list, or None if the list is empty.
        - last:  Event object representing the last event in the linked list, or None if the list is empty.
        - current: The current active event pointer for supporting undo functionality.
        - full_log: A list of strings recording all commands (including undo) in chronological order.

    Representation Invariants:
        - If the list is not empty, `first` and `last` must not be None.
        - If the list is empty, both `first` and `last` must be None.
        - All nodes in the list must form a valid doubly linked list:
          Each node's `next` and `prev` references must correctly point to the next and previous nodes.
        - The `next` reference of the last node must be None.
        - The `prev` reference of the first node must be None.
    """
    first: Optional[Event]
    last: Optional[Event]
    current: Optional[Event]
    full_log: list[str]

    def __init__(self) -> None:
        """Initialize a new empty event list."""
        self.first = None
        self.last = None
        self.current = None
        self.full_log = []

    def display_events(self) -> None:
        """
        Display all commands (including undo) stored in full_log.
        This shows the chronological record of actions.
        """
        print("Full Command Log:")
        for record in self.full_log:
            print(record)

    def undo_last_event(self) -> Optional[Event]:
        """
        Undo the last event by moving the 'current' pointer one step backward.
        This does not delete the event node, allowing for unlimited undo.
        """
        if self.current is None:
            print("No events to undo.")
            self.full_log.append("Attempted undo: No events to undo.")
            return None

        undone_event = self.current
        # Record this undo operation in full_log
        self.full_log.append(f"Undo: {undone_event.next_command} (Location: {undone_event.id_num})")
        self.current = self.current.prev  # Move the current pointer back
        print(f"🔄 Undo: {undone_event.next_command}")
        return undone_event

    def is_empty(self) -> bool:
        """Return whether this event list is empty."""
        return self.first is None

    def add_event(self, event: Event, command: str = None) -> None:
        """
        Add the given new event to the end of this event list.
        The given command is the command which was used to reach this new event,
        or None if this is the first event in the game.

        If there are undone events (current is not the last), remove them.
        Then append the new event, update current to the new event, and record it in full_log.
        """
        # If the current pointer is not the last, discard future events
        if self.current is not None and self.current != self.last:
            temp = self.current.next
            while temp:
                next_temp = temp.next
                temp.prev = None
                temp.next = None
                temp = next_temp
            self.current.next = None
            self.last = self.current

        # If list is empty, initialize
        if self.first is None:
            self.first = event
            self.last = event
            self.current = event
        else:
            # Link new event at the end of the list
            self.last.next_command = command
            self.last.next = event
            event.prev = self.last
            self.last = event
            self.current = event

        # Record the command if it exists
        if command:
            self.full_log.append(f"Command: {command} (Location: {event.id_num})")

    def remove_last_event(self) -> None:
        """
        Remove the last event from this event list.
        If the list is empty, do nothing.
        """
        if self.is_empty():
            return
        if self.first == self.last:
            self.first = self.last = None
        else:
            self.last = self.last.prev
            self.last.next = None
            self.last.next_command = None

    def get_id_log(self) -> list[int]:
        """
        Return a list of all location IDs visited for each event in this list, in sequence.
        """
        id_log = []
        curr = self.first
        while curr:
            id_log.append(curr.id_num)
            curr = curr.next
        return id_log


if __name__ == "__main__":
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })
