from __future__ import annotations
from typing import ClassVar

import os
import csv


class Config:
    BOOKINGS_FILE: ClassVar[str] = os.path.join(os.path.dirname(__file__), "data", "bookings_final_state.csv")
    NEWLINE: ClassVar[str] = ""
    DELIMITER: ClassVar[str] = ","
    LIST_DELIMITER: ClassVar[str] = "|"


class Room:

    rooms: ClassVar[dict[str, Room]] = {}

    def __init__(self, room_no: str, building: str, capacity: int, booked_hours: tuple[bool, ...] | None = None) -> None:
        self.room_no: str = room_no
        self.building: str = building
        self.capacity: int = capacity
        if booked_hours:
            self.booked_hours: tuple[bool, ...] = booked_hours
        else:
            self.booked_hours: tuple[bool, ...] = ()

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
    def split(booked_hours: str) -> tuple[bool, ...]:
        return tuple([bool(item) for item in booked_hours.split(Config.LIST_DELIMITER)])
    
    @staticmethod
    def join(booked_hours: tuple[bool, ...]) -> str:
        out: str = ""
        for i in range(len(booked_hours)):
            if i != 0:
                out += Config.LIST_DELIMITER
            out += str(int(booked_hours[i]))
        return out


def main():
    Room.load()

if __name__ == "__main__":
    main()
