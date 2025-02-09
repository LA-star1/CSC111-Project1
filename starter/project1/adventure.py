
"""CSC111 Project 1: Text Adventure Game - Game Manager

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

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
import json
from typing import Optional

from dataclasses import dataclass, field
from game_entities import Location, Item
from proj1_event_logger import Event, EventList
# from dataclasses import asdict
# Note: You may add in other import statements here as needed

# Note: You may add helper functions, classes, etc. below as needed


@dataclass
class PlayerStatus:
    """
    Represents the status of a player in the text adventure game.

    Attributes:
        score (int): The current score of the player.
        moves (int): The number of moves the player has made.
        max_moves (int): The maximum allowed moves before the game is over.
        inventory (set[str]): The set of items collected by the player.
    """
    score: int = 0
    moves: int = 0
    max_moves: int = 60
    inventory: set[str] = field(default_factory=set)
    inventory_capacity: int = 3


@dataclass
class GameSettings:
    """
    Represents the game configuration settings.

    Attributes:
        required_items (set[str]): The set of item names required to win the game.
        dorm_room_id (int): The location ID of the dorm room where required items must be returned.
    """
    required_items: set[str] = field(default_factory=lambda: {"usb drive", "laptop", "t-card", "laptop charger"})
    dorm_room_id: int = 1203


class AdventureGame:
    """A text adventure game class storing all location, item and map data.

    Instance Attributes:
        - _locations (dict[int, Location]): Maps each unique location ID
            to a Location object representing places in the game.
        - _items (list[Item]): Contains all interactable items within the game.
        - current_location_id (int): ID of the current location of the player, must be a valid key in _locations.
        - ongoing (bool): Flag indicating whether the game is still active.

    Representation Invariants:
         - All keys in _locations are unique and correspond to only one Location object each.
        - current_location_id is always a valid key in the _locations dictionary.
        - Items in _items list are placed correctly according to their game logic (if applicable).

    """

    # Private Instance Attributes (do NOT remove these two attributes):
    #   - _locations: a mapping from location id to Location object.
    #                       This represents all the locations in the game.
    #   - _items: a list of Item objects, representing all items in the game.

    _locations: dict[int, Location]
    _items: list[Item]
    current_location_id: int  # Suggested attribute, can be removed
    ongoing: bool  # Suggested attribute, can be removed

    player_status: PlayerStatus
    game_settings: GameSettings
    game_log: EventList

    def __init__(self, game_data_file: str, initial_location_id: int) -> None:
        """
        Initialize a new text adventure game, based on the data in the given file, setting starting location of game
        at the given initial location ID.
        (note: you are allowed to modify the format of the file as you see fit)

        Preconditions:
        - game_data_file is the filename of a valid game data JSON file
        """

        # NOTES:
        # You may add parameters/attributes/methods to this class as you see fit.

        # Requirements:
        # 1. Make sure the Location class is used to represent each location.
        # 2. Make sure the Item class is used to represent each item.

        # Suggested helper method (you can remove and load these differently if you wish to do so):
        self._locations, self._items = self._load_game_data(game_data_file)

        # Suggested attributes (you can remove and track these differently if you wish to do so):
        self.current_location_id = initial_location_id  # game begins at this location
        self.ongoing = True  # whether the game is ongoing
        # 使用数据类封装玩家状态与游戏设定
        self.player_status = PlayerStatus()  # 包含 score, moves, max_moves, inventory 等信息
        self.game_settings = GameSettings()  # 包含 required_items, dorm_room_id 等信息

        self.game_log = EventList()  # 事件日志

    @staticmethod
    def _load_game_data(filename: str) -> tuple[dict[int, Location], list[Item]]:
        """Load locations and items from a JSON file with the given filename and
        return a tuple consisting of (1) a dictionary of locations mapping each game location's ID to a Location object,
        and (2) a list of all Item objects."""

        with open(filename, 'r') as f:
            data = json.load(f)  # This loads all the data from the JSON file

        locations = {}
        for loc_data in data['locations']:  # Go through each element associated with the 'locations' key in the file
            location_obj = Location(loc_data['id'], loc_data['name'], loc_data['brief_description'],
                                    loc_data['long_description'],
                                    loc_data['available_commands'], loc_data['items'])
            locations[loc_data['id']] = location_obj

        items = []
        for item_data in data['items']:
            item_obj = Item(
                item_data['name'],
                item_data['description'],
                item_data['start_position'],
                item_data['target_position'],
                item_data['target_points']
            )
            items.append(item_obj)

        return locations, items

    def get_location(self, loc_id: Optional[int] = None) -> Location:
        """Return Location object associated with the provided location ID.
        If no ID is provided, return the Location object associated with the current location.
        """
        if loc_id is None:
            loc_id = self.current_location_id

        return self._locations[loc_id]

    # def move_player(self, direction: str) -> None:
    #     """玩家移动到指定方向"""
    #     curr_location = self.get_location()
    #     print(f"You are now at: {curr_location.name}")
    #
    #     # 检查目标方向是否在当前地点的 `available_commands`
    #     if direction in curr_location.available_commands:
    #         new_location_id = curr_location.available_commands[direction]
    #         self.current_location_id = new_location_id  # 更新位置
    #         self.player_status.moves += 1   # 增加移动步数
    #
    #         # 记录事件日志
    #         self.game_log.add_event(Event(new_location_id, f"Moved {direction} to {self.get_location().name}"))
    #
    #         print(f"You moved {direction}. Moves used: {self.player_status.moves}/{self.player_status.max_moves}")
    #
    #         # 检查是否赢/输
    #         self.check_game_status()
    #     else:
    #         print("You can't go that way.")

    # def print_map(self) -> None:
    #     """在报告中打印游戏地图"""
    #     grid = [
    #         [1, 2, -1],
    #         [4, -1, -1]
    #     ]
    #
    #     print("\nGame Map:")
    #     for row in grid:
    #         print(" ".join(str(cell) for cell in row))

    def check_game_status(self) -> None:
        """检查玩家是否赢得或输掉游戏"""

        # 1️⃣ 检查是否超出最大步数（输）
        if self.player_status.moves >= self.player_status.max_moves:
            print("🕓 Time's up! It's 4 PM, and the project deadline has passed. You lost! 😢")
            self.ongoing = False
            return

        # 2️⃣ 检查是否满足获胜条件（赢）
        elif (self.game_settings.required_items.issubset(self.player_status.inventory)
                and self.current_location_id == 1203):
            print("🎉 Congratulations! You returned all required items before the deadline! You win! 🏆")
            self.ongoing = False

    def add_score(self, points: int) -> None:
        """增加玩家分数"""
        self.player_status.score += points
        print(f"You earned {points} points! Current score: {self.player_status.score}")

    def pick_up_item(self, item_name: str) -> None:
        """Allow the player to pick up an item and update the score."""
        curr_location = self.get_location()
        print(f"You are now at: {curr_location.name}")

        if curr_location.items is None or not any(it.lower() == item_name.lower() for it in curr_location.items):
            print(f"{item_name} is not at this location.")
            return

        for item in self._items:
            # 判断玩家输入的物品名称是否与当前物品匹配，并且该物品应出现在当前地点
            if item.name.lower() == item_name.lower() and item.start_position == curr_location.id_num:

                # 如果物品不是咖啡，并且玩家已经拥有该物品，则不允许重复拾取
                if item.name.lower() != "coffee" and item.name.lower() in self.player_status.inventory:
                    print(f"You have already picked up {item_name}.")
                    return

                # 对于非咖啡、非书包物品，检查库存容量
                if item.name.lower() != "backpack" and item.name.lower() != "coffee":
                    if len(self.player_status.inventory) >= self.player_status.inventory_capacity:
                        print("Your inventory is full! You cannot pick up more items.")
                        return

                # 如果当前地点的物品列表中存在该物品，则移除它，确保物品不再重复出现在房间里
                if curr_location.items and item_name in curr_location.items:
                    curr_location.items.remove(item_name)

                # 针对咖啡，执行特殊处理：直接消耗，不计入库存，而是增加移动步数和分数
                if item.name.lower() == "coffee":
                    self.player_status.max_moves += 20  # 增加额外的移动步数
                    self.add_score(5)  # 分数奖励
                    print(
                        f"You picked up and drank a coffee! Your max moves increased by 5 "
                        f"to {self.player_status.max_moves}.")
                    self.check_game_status()
                    return

                # 添加到玩家库存中
                self.player_status.inventory.add(item_name.lower())
                self.add_score(10)  # 拾取物品奖励 +10 分
                print(f"You picked up {item_name}. Your inventory: {', '.join(self.player_status.inventory)}")

                # 如果拾取的是书包，则增加库存容量（例如增加 3 个槽）
                if item.name.lower() == "backpack":
                    self.player_status.inventory_capacity += 3
                    print(
                        f"Your backpack increases your inventory capacity "
                        f"to {self.player_status.inventory_capacity} items.")

                self.check_game_status()
                return

        print(f"{item_name} is not at this location.")

    def deposit_item(self, item_name: str) -> None:
        """Allow the player to deposit an item at the correct location for points."""
        if item_name not in self.player_status.inventory:
            print(f"You don't have {item_name} in your inventory.")
            return

        curr_location = self.get_location()
        print(f"You are now at: {curr_location.name}")

        for item in self._items:
            if item.name.lower() == item_name.lower() and item.target_position == curr_location.id_num:
                self.player_status.inventory.remove(item_name)
                self.add_score(item.target_points)
                print(f"You deposited {item_name} at {curr_location.name}. Earned {item.target_points} points!")
                self.check_game_status()
                if self.player_status.score >= 300:
                    print("Thanks for the trophy and red bull! the passcode for the safe in "
                          "the computer lab is:\"csc is the best!\" ")
                return

        print(f"{item_name} cannot be deposited here.")

    def show_score(self) -> None:
        """Display the player's current score."""
        print(f"Your current score is: {self.player_status.score}")

    def quit_game(self) -> None:
        """Handle quitting the game."""
        print("Thank you for playing! Exiting the game now...")
        self.ongoing = False

    def enter_password(self) -> None:
        """
        如果玩家位于 Robarts Study Rooms（ID 3902），提示输入密码以解锁房间，
        并将隐藏的电脑添加到该房间的物品列表中。
        """
        # 检查当前所在位置是否为 3902
        if self.current_location_id != 3902 and self.current_location_id != 4206:
            print("There is no password-protected area here.")
            return

        # 提示玩家输入密码
        password = input("Enter password to unlock the room: ").strip()
        # 预设密码（你可以修改为你想要的密码）
        if self.current_location_id == 3902:
            correct_password = "12345678"
            if password == correct_password:
                loc = self.get_location()
                # 如果当前地点的 items 为空，则创建一个列表
                if loc.items is None:
                    loc.items = []
                # 如果电脑还未添加，则将 "laptop" 添加到该地点的 items 中
                if "laptop" not in loc.items:
                    loc.items.append("laptop")
                    print("The room is unlocked! The laptop is now available.")
                else:
                    print("The room is already unlocked.")
            else:
                print("Incorrect password!")

        elif self.current_location_id == 4206:
            correct_password = "csc is the best!"
            if password == correct_password:
                loc = self.get_location()
                # 如果当前地点的 items 为空，则创建一个列表
                if loc.items is None:
                    loc.items = []
                # 如果电脑还未添加，则将 "computer" 添加到该地点的 items 中
                if "computer" not in loc.items:
                    loc.items.append("usb drive")
                    print("The room is unlocked! The usb drive is now available.")
                else:
                    print("The room is already unlocked.")
            else:
                print("Incorrect password!")


if __name__ == "__main__":

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999']
    # })

    game_log = EventList()  # This is REQUIRED as one of the baseline requirements
    game = AdventureGame('game_data.json', 1203)  # load data, setting initial location ID to 1
    menu = ["look", "inventory", "score", "undo", "log", "quit", "pick up", "drop", "unlock"]
    # Regular menu options available at each location
    choice = "start"

    # Note: You may modify the code below as needed; the following starter code is just a suggestion
    while game.ongoing:
        # Note: If the loop body is getting too long, you should split the body up into helper functions
        # for better organization. Part of your marks will be based on how well-organized your code is.

        location = game.get_location()

        if choice is not None:
            event_command = choice
        else:
            event_command = "start"
        current_event = Event(id_num=location.id_num, description=location.long_description, next_command=event_command)
        game_log.add_event(current_event)

        if location.visited:
            print(location.brief_description)
        else:
            print(location.long_description)
            location.visited = True

        # Display possible actions at this location
        print("What to do? Choose from: look, inventory, score, undo, log, quit, pick up, drop, unlock")
        print("At this location, you can also:")
        for action in location.available_commands:
            print("-", action)

        # Validate choice
        choice = input("\nEnter action: ").lower().strip()
        while choice not in location.available_commands and choice not in menu:
            print("That was an invalid option; try again.")
            choice = input("\nEnter action: ").lower().strip()

        print("========")
        print("You decided to:", choice)

        if choice in menu:
            # Note: For the "undo" command, remember to manipulate the game_log event list to keep it up-to-date
            # ENTER YOUR CODE BELOW to handle other menu commands (remember to use helper functions as appropriate)
            if choice == "log":
                game_log.display_events()
            elif choice == "quit":
                print("Exiting game.")
                game.ongoing = False
            elif choice == "score":
                game.show_score()
            elif choice == "look":
                print(game.get_location().long_description)
            elif choice == "inventory":
                inv = game.player_status.inventory
                print("Your inventory:", ", ".join(inv) if inv else "Empty")
            elif choice == "undo":
                game.game_log.undo_last_event()
            elif choice == "pick up":
                item_name = input("Which item do you want to pick up? ").lower().strip()
                if item_name:
                    game.pick_up_item(item_name)
                else:
                    print("No item specified.")
            elif choice == "drop":
                item_name = input("Which item do you want to drop? ").lower().strip()
                if item_name:
                    game.deposit_item(item_name)
                else:
                    print("No item specified.")
            elif choice == "unlock":
                game.enter_password()

        else:
            # Handle non-menu actions
            if choice in location.available_commands:
                game.current_location_id = location.available_commands[choice]
                game.player_status.moves += 1
                print("Moving to:", game.get_location().name)
            else:
                print("Action not recognized.")

            result = location.available_commands[choice]
            game.current_location_id = result

        print("========")
        game.check_game_status()
