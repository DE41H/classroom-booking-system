from __future__ import annotations
from typing import ClassVar, Callable

import os
import csv
from time import sleep


class NotAnOption(Exception):

    def __init__(self, message: str) -> None:
        self.message: str = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f'Error: {self.message} is not a valid option!\nTry Again...'
    
class NaN(Exception):

    def __init__(self, message: str) -> None:
        self.message: str = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f'Error: {self.message} is not a numeric value!\nTry Again...'
    

class RoomNotFoundError(Exception):

    def __init__(self, room_no: str) -> None:
        self.room_no: str = room_no
        super().__init__(self.room_no)

    def __str__(self) -> str:
        return f'Error: Room {self.room_no} does not exist!\nTry Again...'


class RoomAlreadyExistsError(Exception):

    def __init__(self, room_no: str) -> None:
        self.room_no: str = room_no
        super().__init__(self.room_no)

    def __str__(self) -> str:
        return f'Error: Room {self.room_no} already exists!\nTry Again...'


class TimeslotAlreadyBookedError(Exception):

    def __init__(self, room_no: str, hour: int) -> None:
        self.room_no: str = room_no
        self.hour: int = hour
        super().__init__(self.room_no)

    def __str__(self) -> str:
        return f'Error: {self.room_no} is already booked from {self.hour}:00 - {self.hour + 1}:00!\nTry booking a different slot'


class Config:
    BOOKINGS_FILE: ClassVar[str] = os.path.join(os.path.dirname(__file__), "data", "bookings_final_state.csv")
    NEWLINE: ClassVar[str] = ""
    DELIMITER: ClassVar[str] = ","
    LIST_DELIMITER: ClassVar[str] = ";"
    DELAY: ClassVar[float] = 1.0


class Menu:

    running: ClassVar[bool] = True
    
    def __init__(self) -> None:
        self.options: dict[int, str] = {
            1: "View Room",
            2: "Book Room",
            3: "Create Room",
            4: "Find Room",
            0: "Exit"
        }
        self.functions: dict[int, Callable[[], None]] = {
            1: self.view,
            2: self.book,
            3: self.create,
            4: self.find,
            0: self.exit
        }
        
    def __repr__(self) -> str:
        return str(int(self.running))

    def clear(self) -> None:
        if os.name == "nt":
            os.system("cls")
        else:
            print("\033[H" + "\033[J" + "\033[3J")

    def menu(self) -> None:
        while self.running:
            try:
                self.clear()
                print("\n============= [ MAIN MENU ] =============\n")
                for option in self.options:
                    print(f'[{option}] {self.options[option]}')
                choice: str = input("\nEnter Option ID: ")
                if not choice.isdigit():
                    raise NaN(choice)
                option: int = int(choice)
                func: Callable[[], None] | None = self.functions.get(option)
                if func:
                    func()
                else:
                    raise NotAnOption(choice)
                break
            except (NotAnOption, NaN) as err:
                print(err)
                sleep(Config.DELAY)
            finally:
                choice: str = input("Press ENTER to abort...\nEnter text to retry: ")
                if choice == "":
                    break
                else:
                    continue
                
            
    def view(self) -> None:
        while True:
            try:
                self.clear()
                print("\n============= [ VIEW ROOM ] =============\n")
                room_no: str = input("Enter Room Number: ")
                if Room.exists(room_no):
                    print(Room.view(room_no))
                    return
                else:
                    choice: str = input("Press ENTER to abort...\nEnter text to retry: ")
                if choice == "":
                    Menu.running = False
                else:
                    raise RoomNotFoundError(room_no)
            except (RoomNotFoundError) as err:
                print(err)
                sleep(Config.DELAY)
            finally:
                choice: str = input("Press ENTER to abort...\nEnter text to retry: ")
                if choice == "":
                    break
                else:
                    continue

    def book(self):
        while True:
            try:
                self.clear()
                print("\n============= [ BOOK ROOM ] =============\n")
                room_no: str = input("Enter Room Number: ")
                if not Room.exists(room_no):
                    raise RoomNotFoundError(room_no)
                Room.display_hours()
                hour: int = 0
                while True:
                    try:
                        choice: str = input("Enter booking hour: ")
                        if not choice.isdigit():
                            raise NaN(choice)
                        hour: int = int(choice)
                        if hour not in range(24):
                            raise NotAnOption(str(hour))
                    except (NaN, NotAnOption) as err:
                        print(err)
                        sleep(Config.DELAY)
                    finally:
                        choice: str = input("Press ENTER to abort...\nEnter text to retry: ")
                        if choice == "":
                            break
                        else:
                            continue
                booked: bool = Room.book(room_no, hour)
                if booked:
                    return
                else:
                    raise TimeslotAlreadyBookedError(room_no, hour)
            except (RoomNotFoundError, TimeslotAlreadyBookedError) as err:
                print(err)
                sleep(Config.DELAY)
            finally:
                choice: str = input("Press ENTER to abort...\nEnter text to retry: ")
                if choice == "":
                    break
                else:
                    continue
                

    def create(self):
        while True:
            try:
                self.clear()
                print("\n============= [ CREATE ROOM ] =============\n")
                room_no: str = input("Enter Room Number: ")
                if Room.exists(room_no):
                    raise RoomAlreadyExistsError(room_no)
                building: str = input("Enter Building: ")
                capacity: str = ""
                while True:
                    try:
                        capacity: str = input("Enter Capacity: ")
                        if capacity.isdigit():
                            break
                        else:
                            raise NaN(capacity)
                    except NaN as err:
                        print(err)
                        sleep(Config.DELAY)
                    finally:
                        choice: str = input("Press ENTER to abort...\nEnter text to retry: ")
                        if choice == "":
                            break
                        else:
                            continue
                Room.create(room_no, building, int(capacity))
            except RoomAlreadyExistsError as err:
                print(err)
                sleep(Config.DELAY)
            finally:
                choice: str = input("Press ENTER to abort...\nEnter text to retry: ")
                if choice == "":
                    break
                else:
                    continue

    def find(self):
        while True:
            try:
                self.clear()
                print("\n============= [ FIND ROOM ] =============\n")
                options: dict[int, str] = {
                    1: "Search by building",
                    2: "Search by capacity",
                    3: "Search by hour",
                    0: "Return" 
                }
                for option in options:
                    print(f'[{option}] {options[option]}')
                choice: str = input("\nEnter Option Number: ")
                if not choice.isdigit():
                    raise NaN(choice)
                option: int = int(choice)
                if option not in options:
                    raise NotAnOption(choice)
                match option:
                    case 1:
                        building: str = input("Enter Building: ")
                        rooms: set[Room] = Room.by_building(building)
                        if len(rooms):
                            print(f'Rooms available in {building}: {rooms}')
                        else:
                            print(f'No rooms available in {building}')
                    case 2:
                        while True:
                            try:
                                capacity: str = input("Enter required Capacity: ")
                                if not capacity.isdigit():
                                    raise NaN(choice)
                                rooms: set[Room] = Room.by_capacity(int(capacity))
                                if len(rooms):
                                    print(f'Rooms available with capacity of {rooms}: {rooms}')
                                else:
                                    print(f'No rooms available with capacity of {capacity}')
                            except RoomAlreadyExistsError as err:
                                print(err)
                                sleep(Config.DELAY)
                            finally:
                                choice: str = input("Press ENTER to abort...\nEnter text to retry: ")
                                if choice == "":
                                    break
                                else:
                                    continue
                    case 3:
                        while True:
                            try:
                                choice: str = input("Enter hour: ")
                                if not choice.isdigit():
                                    raise NaN(choice)
                                hour: int = int(choice)
                                print(Room.display_hours())
                                rooms: set[Room] = Room.by_hour(hour)
                                if len(rooms):
                                    print(f'Rooms available from {hour}:00 to {hour + 1}:00: {rooms}')
                                else:
                                    print(f'No rooms available with from {hour}:00 to {hour + 1}:00')
                            except NaN as err:
                                print(err)
                                sleep(Config.DELAY)
                            finally:
                                choice: str = input("Press ENTER to abort...\nEnter text to retry: ")
                                if choice == "":
                                    break
                                else:
                                    continue
                    case 0:
                        break
                    case _:
                        pass
            except (NaN, NotAnOption) as err:
                print(err)
                sleep(Config.DELAY)
            finally:
                choice: str = input("Press ENTER to abort...\nEnter text to retry: ")
                if choice == "":
                    break
                else:
                    continue

    @classmethod
    def exit(cls):
        Room.save()
        cls.running = False


class Room:

    rooms: ClassVar[dict[str, Room]] = {}

    def __init__(self, room_no: str, building: str, capacity: int, booked_hours: list[bool] = [False] * 24) -> None:
        self.room_no: str = room_no
        self.building: str = building
        self.capacity: int = capacity
        self.booked_hours: list[bool] = booked_hours

    def __repr__(self) -> str:
        return f'Room No.: {self.room_no}, Building: {self.building}, Capacity: {self.capacity}'

    @classmethod
    def load(cls) -> None:
        while True:
            try:
                with open(Config.BOOKINGS_FILE, "r", newline=Config.NEWLINE) as file:
                    reader = csv.DictReader(file, delimiter=Config.DELIMITER)
                    for row in reader:
                        cls.rooms[row["room_no"]] = Room(row["room_no"], row["building"], int(row["capacity"]), cls.split(row["booked_hours"]))
                break
            except FileNotFoundError:
                print(f'Error: {Config.BOOKINGS_FILE} not found')
            except (ValueError, csv.Error, KeyError):
                print(f'Error: Data format error in {Config.BOOKINGS_FILE}')
            except (IOError, Exception):
                print(f'Error: Problem loading {Config.BOOKINGS_FILE}')
            finally:
                choice: str = input("Press ENTER to abort...\nEnter text to retry: ")
                if choice == "":
                    Menu.running = False
                    break
                else:
                    continue

    @classmethod
    def save(cls) -> None:
        while True:
            try:
                with open(Config.BOOKINGS_FILE, "w", newline=Config.NEWLINE) as file:
                    writer = csv.writer(file)
                    header: list[str] = ["room_no", "building", "capacity", "booked_hours"]
                    writer.writerow(header)
                    for room_no, room in cls.rooms.items():
                        writer.writerow([room_no, room.building, str(room.capacity), cls.join(room.booked_hours)])
            except FileNotFoundError:
                print(f'Error: {Config.BOOKINGS_FILE} not found')
            except PermissionError:
                print(f'Error: Lacking permission to write to {Config.BOOKINGS_FILE}')
            except (ValueError, csv.Error, KeyError):
                print(f'Error: Data format error in {Config.BOOKINGS_FILE}')
            except (IOError, Exception):
                print(f'Error: Problem loading {Config.BOOKINGS_FILE}')
            finally:
                choice: str = input("Press ENTER to abort...\nEnter text to retry: ")
                if choice == "":
                    Menu.running = False
                else:
                    continue

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
        room: Room = cls.rooms[room_no]
        if not room.booked_hours[hour]:
            room.booked_hours[hour] = True
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
        return Config.LIST_DELIMITER.join([str(int(item)) for item in booked_hours])
    
    @staticmethod
    def display_hours(booked_hours: list[bool] | None = None) -> str:
        out: str = ""
        for i in range(24):
            factor: str = ""
            if booked_hours:
                factor = f' => {"Booked" if booked_hours[i] else "Available"}'
            else:
                factor = ""
            out += f'[{i}] {i}:00 to {i + 1}:00 => ' + factor + "\n"
        return out


def main():
    Room.load()
    menu: Menu = Menu()
    menu.menu()

if __name__ == "__main__":
    main()
