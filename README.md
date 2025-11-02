# 🏫 CLASSROOM BOOKING SYSTEM

A simple yet efficient **command-line Classroom Booking System** built in Python.  
It allows users to **view**, **book**, **create**, and **search for rooms** interactively — while maintaining persistent records via a CSV database.

---

## ✨ Features

### 🧭 Interactive Menu
Easily navigate the system through an intuitive menu-driven interface:
```
============= [ MAIN MENU ] =============
[1] View Room
[2] Book Room
[3] Create Room
[4] Find Room
[0] Exit
```

### 🏠 Room Management
- **Create new rooms** by specifying:
  - Room number
  - Building name
  - Capacity
- Prevents duplication with proper error handling (`RoomAlreadyExistsError`).

### 📅 Booking System
- **Book hourly timeslots** for any room (24-hour format).
- Automatically prevents **double-booking** using `TimeslotAlreadyBookedError`.
- Shows availability clearly with labels for each hour.

### 🔍 Search & Find Rooms
- Find rooms **by building**, **by capacity**, or **by available hour**.
- Get neatly formatted lists of available rooms matching your criteria.

### 📋 Persistent Data Storage
- Room and booking data are stored in a CSV file:  
  `data/bookings_final_state.csv`
- Automatically loads and saves data with each session.
- Safe error handling for file operations (e.g., missing files, permission issues).

### ⚙️ Configurable Constants
Easily adjust application behavior via the `Config` class:
```python
class Config:
    BOOKINGS_FILE = "data/bookings_final_state.csv"
    NEWLINE = ""
    DELIMITER = ","
    LIST_DELIMITER = ";"
    DELAY = 1.0
```

---

## 🧩 Project Structure

```
CLASSROOM_BOOKING_SYSTEM/
├── data/
│   └── bookings_final_state.csv        # Persistent room booking data
├── bookings.py                         # Core program logic
├── requirements.txt                    # Python dependencies
├── LICENSE                             # License file
├── .gitignore                          # Git ignore rules
```

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/DE41H/CLASSROOM_BOOKING_SYSTEM.git
cd CLASSROOM_BOOKING_SYSTEM
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Program
```bash
python bookings.py
```

---

## 🧠 Usage Examples

### ▶️ Create a Room
```
============= [ CREATE ROOM ] =============
Enter Room Number: FD1-1223
Enter Building: FD1
Enter Capacity: 40
```

### 🕐 Book a Room
```
============= [ BOOK ROOM ] =============
Enter Room Number: FD1-1223
[0] 0:00 to 1:00 => Available
...
Enter booking hour: 10
Room A101 has been booked from 10:00 to 11:00
```

### 🔎 Find Rooms
```
============= [ FIND ROOM ] =============
[1] Search by building
[2] Search by capacity
[3] Search by hour
[0] Return
```

---

## 🧰 Error Handling

Custom exceptions ensure smooth operation:
- `NotAnOption` — Invalid menu selection
- `NaN` — Non-numeric capacity or hour input
- `RoomNotFoundError` — Room does not exist
- `RoomAlreadyExistsError` — Duplicate room
- `TimeslotAlreadyBookedError` — Slot already taken

---

## 🪶 License
This project is licensed under the terms specified in the [LICENSE](./LICENSE) file.

---

