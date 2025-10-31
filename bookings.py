from __future__ import annotations
from typing import ClassVar, Callable

import os
import csv
import time


class NotAnOption(Exception):

    def __init__(self, message: str, end: str) -> None:
        self.message: str = message
        self.end: str = end
        super().__init__(self.message)
        print(self)
        time.sleep(Config.DELAY)

    def __repr__(self) -> str:
        return f'Error: {self.message} is not a valid option! {self.end}'
    

class RoomNotFoundError(Exception):

    def __init__(self, room_no: str, end: str) -> None:
        self.room_no: str = room_no
        self.end: str = end
        super().__init__(self)
        print(self)
        time.sleep(Config.DELAY)

    def __repr__(self) -> str:
        return f'Error: There exists no Room with Room Number {self.room_no} {self.end}'


class RoomAlreadyExistsError(RoomNotFoundError):

    def __repr__(self) -> str:
        return f'Error: There already exists Room with Room Number {self.room_no} {self.end}'


class TimeslotAlreadyBookedError(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class Config:
    BOOKINGS_FILE: ClassVar[str] = os.path.join(os.path.dirname(__file__), "data", "bookings_final_state.csv")
    NEWLINE: ClassVar[str] = ""
    DELIMITER: ClassVar[str] = ","
    LIST_DELIMITER: ClassVar[str] = ";"
    DELAY: ClassVar[float] = 1.0


class Menu:
    
    def __init__(self) -> None:
        self.options: dict[int, str] = {}
        self.functions: dict[int, Callable[[], None]] = {}
        self.running: bool = True

    def __repr__(self) -> str:
        return str(int(self.running))

    def clear(self) -> None:
        if os.name == "nt":
            os.system("cls")
            return ""
        else:
            print("\033[H" + "\033[J" + "\033[3J")

    def menu(self) -> None:
        while self.running:
            self.clear()
            print("\n============= [ Main Menu ] =============n")
            for option in self.options:
                print(f'[{option}] {self.options[option]}')
            choice: str = input("\nEnter Option ID: ")
            if choice.isdigit() and int(choice) in self.options:
                option: int = int(choice)
                func: Callable[[], None] | None = self.functions.get(option)
                if func:
                    func()
            else:
                raise NotAnOption(choice, "\nChoose a valid option! Try Again...")
            
    def view(self) -> None:
        while True:
            self.clear()
            room_no: str = input("Enter Room Number: ")
            if Room.exists(room_no):
                print(Room.view(room_no))
                return
            else:
                raise RoomNotFoundError(room_no, "\nTry Again...")

    def book(self):
        while True:
            self.clear()
            room_no: str = input("Enter Room Number: ")
            Room.display_hours()
            choice: str = input("Enter booking hour: ")
            if choice.isdigit() and int(choice) in range(24):
                if Room.exists(room_no):
                    hour: int = int(choice)
                    booked: bool = Room.book(room_no, hour)
                    if booked:
                        return
                    else:
                        raise TimeslotAlreadyBookedError(room_no, hour)
            else:
                raise NotAnOption(choice, "\nChoose a valid option! Try Again...")
                

    def create(self):
        pass

    def find(self):
        pass

    def exit(self):
        self.running = False


class Room:

    rooms: ClassVar[dict[str, Room]] = {}

    def __init__(self, room_no: str, building: str, capacity: int, booked_hours: list[bool] | None = None) -> None:
        self.room_no: str = room_no
        self.building: str = building
        self.capacity: int = capacity
        if booked_hours:
            self.booked_hours: list[bool] = booked_hours
        else:
            self.booked_hours: list[bool] = []

    @classmethod
    def load(cls) -> None:
        with open(Config.BOOKINGS_FILE, "r", newline=Config.NEWLINE) as file:
            reader = csv.DictReader(file, delimiter=Config.DELIMITER)
            for row in reader:
                cls.rooms[row["room_no"]] = Room(row["room_no"], row["building"], int(row["capacity"]), cls.split(row["booked_hours"]))

    @classmethod
    def save(cls) -> None:
        with open(Config.BOOKINGS_FILE, "w", newline=Config.NEWLINE) as file:
            writer = csv.writer(file)
            header: list[str] = ["room_ no", "building", "capacity", "booked_hours"]
            writer.writerow(header)
            for room_no, room in cls.rooms.items():
                writer.writerow([room_no, room.building, str(room.capacity), cls.join(room.booked_hours)])

    @classmethod
    def create(cls, room_no: str, building: str, capacity: int) -> bool:
        if room_no not in cls.rooms:
            cls.rooms[room_no] = Room(room_no, building, capacity)
            return True
        else:
            return False
        
    @classmethod
    def view(cls, room_no: str) -> str:
        out: str = ""
        room: Room = cls.rooms[room_no]
        out += "Room Number => " + room.room_no + "\n"
        out += "Building => " + room.building + "\n\n"
        out += "Bookings:\n"
        cls.display_hours(room.booked_hours)
        return out

    @classmethod
    def book(cls, room_no: str, hour: int) -> bool:
        if cls.rooms[room_no] in cls.by_hour(hour):
            cls.rooms[room_no].booked_hours[hour] = True
            return True
        else:
            return False
        
    @classmethod
    def exists(cls, room_no: str) -> bool:
        return room_no in cls.rooms

    @classmethod
    def by_building(cls, building: str) -> set[Room]:
        rooms: set[Room] = set()
        for room in cls.rooms.values():
            if room.building.lower() == building.lower():
                rooms.add(room)
        return rooms
    
    @classmethod
    def by_capacity(cls, capacity: int) -> set[Room]:
        rooms: set[Room] = set()
        for room in cls.rooms.values():
            if room.capacity >= capacity:
                rooms.add(room)
        return rooms
    
    @classmethod
    def by_hour(cls, hour: int) -> set[Room]:
        rooms: set[Room] = set()
        for room in cls.rooms.values():
            if not room.booked_hours[hour]:
                rooms.add(room)
        return rooms

    @staticmethod
    def split(booked_hours: str) -> list[bool]:
        return [bool(int(item)) for item in booked_hours.split(Config.LIST_DELIMITER)]
    
    @staticmethod
    def join(booked_hours: list[bool]) -> str:
        out: str = ""
        for i in range(24):
            if i != 0:
                out += Config.LIST_DELIMITER
            out += str(int(booked_hours[i]))
        return out
    
    @staticmethod
    def display_hours(booked_hours: list[bool] | None = None) -> str:
        out: str = ""
        for i in range(24):
            factor: str = ""
            if booked_hours:
                factor = f' => {"Booked" if booked_hours[i] else "Available"}'
            else:
                factor = ""
            if i == 0:
                out += f'[{i}] {i}:00A.M. to {i + 1}:00A.M.'
            if i < 11:
                out += f'\n[{i}] {i}:00A.M. to {i + 1}:00A.M.'
            elif i == 11:
                out += f'\n[{i}] {i}:00A.M. to {i + 1}:00P.M.'
            elif i > 11:
                out += f'\n[{i}] {i}:00P.M. to {i + 1}:00P.M.'
            out += factor
        return out


def main():
    Room.load()
    menu: Menu = Menu()
    menu.menu()

if __name__ == "__main__":
    main()
