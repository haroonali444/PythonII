flight_data = {}
user_bookings = []

# Function to save user bookings to a text file
def save_user_bookings():
    with open("user_bookings.txt", "w") as file:
        for booking in user_bookings:
            file.write(f"{booking['Username']},{booking['Flight']},{booking['Seat']}\n")
# Function to load user bookings from a text file
def load_user_bookings():
    try:
        with open("user_bookings.txt", "r") as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 3:
                    booking = {
                        "Username": parts[0],
                        "Flight": parts[1],
                        "Seat": parts[2]
                    }
                    user_bookings.append(booking)
    except FileNotFoundError:
        return

def load_flight_data():
    try:
        with open("flight_data.txt", "r") as file:
            for line in file:
                flight = eval(line)
                flight_data[flight["name"]] = flight
    except FileNotFoundError:
        pass

def save_flight_data(flight_data):
    with open("flight_data.txt", "w") as file:
        for flight_name, flight_details in flight_data.items():
            file.write(str(flight_details) + "\n")

def user_login():
    while True:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        if username == "user" and password == "password":
            return username
        else:
            print("Incorrect login credentials. Try again.")

# User menu
def user_menu(username):
    while True:
        print("\nUser Menu:")
        print("1. Book a Ticket")
        print("2. Display Seat Availability")
        print("3. Book a Seat")
        print("4. Cancel a Booking")
        print("5. Show Flights")
        print("6. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            book_ticket(username)
        elif choice == "2":
            display_seat_availability()
        elif choice == "3":
            book_seat(username)
        elif choice == "4":
            cancel_booking(username)
        elif choice == "5":
            show_flights()
        elif choice == "6":
            return
        else:
            print("Invalid choice. Try again.")
# Function to cancel a booking
def cancel_booking(username):
    flight_name = input("Enter the flight name: ")
    if flight_name in flight_data:
        row = int(input("Enter the row number: ")) - 1
        seat = ord(input("Enter the seat letter (A, B, C, ...): ").upper()) - ord('A')
        
        if 0 <= row < len(flight_data[flight_name]["seats"]) and 0 <= seat < len(flight_data[flight_name]["seats"][row]):

            if flight_data[flight_name]["seats"][row][seat] == "X":
                flight_data[flight_name]["seats"][row][seat] = "*"
                
                # Remove the booking from user_bookings
                booking_to_remove = {
                    "Username": username,
                    "Flight": flight_name,
                    "Seat": f"Row {row + 1}, Seat {seat}",
                }
                if booking_to_remove in user_bookings:
                    user_bookings.remove(booking_to_remove)
                
                save_flight_data(flight_data)
                save_user_bookings()  # Save updated user bookings
                print("Booking canceled successfully.")
            else:
                print("Seat is not booked.")
        else:
            print("Invalid row or seat.")
    else:
        print("Flight not found.")

# Function to book a seat
def book_seat(username):
    flight_name = input("Enter the flight name: ")
    flight = flight_data.get(flight_name)
    if flight:
        row = int(input("Enter the row number: ")) - 1
        seat = ord(input("Enter the seat letter (A, B, C, ...): ").upper()) - ord('A')
        print()

        if 0 <= row or row < len(flight["seats"]) and seat in flight["seats"][row]:
            print(flight["seats"])
            print("Line1")
            print(flight["seats"][row])
            print("Line2")
            print(flight["seats"][row][seat])
            if flight["seats"][row][seat] == "*":
                flight["seats"][row][seat] = "X"
                booking_info = {
                    "Username": username,
                    "Flight": flight_name,
                    "Seat": f"Row {row + 1}, Seat {seat}",
                }
                user_bookings.append(booking_info)
                save_user_bookings()
                print("Seat booked successfully.")
            else:
                print("Seat is already booked.")
        else:
            print("Invalid row or seat.")
    else:
        print("Flight not found.")  
def display_seat_availability():
    flight_name = input("Enter the flight name: ")
    flight = flight_data.get(flight_name)
    if flight:
        seats = flight["seats"]
        for row in seats:
            print(" ".join(row))
    else:
        print("Flight not found.")
def book_ticket(username):
    print("Available Flights:")
    for flight in flight_data.values():
        print(flight["name"])

def show_flights():

    for flight in flight_data.values():
        print(flight["name"])
        print("Departure Time:", flight["departure_time"])
        print("Arrival Time:", flight["arrival_time"])
        print("Seats Available:")
        for row in flight["seats"]:
            print(" ".join(row))
        print()

def admin_login():
    while True:
        username = input("Enter admin username: ")
        password = input("Enter admin password: ")
        if username == "admin" and password == "admin_password":
            return username
        else:
            print("Incorrect admin credentials. Try again.")

def admin_menu(username):
    while True:
        print("\nAdmin Menu:")
        print("1. add flights")
        print("2. remove Flights")
        print("3. Manage Flight Details")
        print("4. Show Flights")
        print("5. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_flight()
        elif choice == "2":
            delete_flight()
        elif choice == "3":
            manage_flight_details()
        elif choice == "4":
            show_flights()
        elif choice == "5":
            return
        else:
            print("Invalid choice. Try again.")
def add_flight():
    flight_name = input("Enter the flight name: ")
    departure_time = input("Enter departure time: ")
    arrival_time = input("Enter arrival time: ")
    seat_layout = [['*' for _ in range(5)] for _ in range(3)]  
    flight_data[flight_name] = {
        "name": flight_name,
        "departure_time": departure_time,
        "arrival_time": arrival_time,
        "seats": seat_layout,
    }
    save_flight_data(flight_data)
    print(f"Flight '{flight_name}' added successfully.")

# Delete Flight Functionality
def delete_flight():
    flight_name = input("Enter the flight name to delete: ")
    if flight_name in flight_data:
        del flight_data[flight_name]
        save_flight_data(flight_data)
        print(f"Flight '{flight_name}' deleted successfully.")
    else:
        print("Flight not found.")

load_flight_data()
load_user_bookings()
def change_seat_layout(flight_name):
    flight = flight_data.get(flight_name)
    if flight:
        rows = int(input("Enter the number of rows: "))
        seats_per_row = int(input("Enter the number of seats per row: "))

        new_seat_layout = [['*' for _ in range(seats_per_row)] for _ in range(rows)]

        flight["seats"] = new_seat_layout
        save_flight_data(flight_data)
        print("Seat layout changed successfully.")
    else:
        print("Flight not found.")
def manage_flight_details():
    flight_name = input("Enter the flight name to manage details: ")
    if flight_name in flight_data:
        print("Flight Details:")
        print(f"Flight Name: {flight_name}")
        print(f"Departure Time: {flight_data[flight_name]['departure_time']}")
        print(f"Arrival Time: {flight_data[flight_name]['arrival_time']}")
        print("1. Change Arrival Time")
        print("2. Change Departure Time")
        print("3. Change Flight Details")
        print("4. Change Seat Layout")
        admin_choice = input("Enter your choice: ")

        if admin_choice == "1":
            new_arrival_time = input("Enter new arrival time: ")
            flight_data[flight_name]["arrival_time"] = new_arrival_time
            save_flight_data(flight_data)
            print("Arrival time updated successfully.")
        elif admin_choice == "2":
            new_departure_time = input("Enter new departure time: ")
            flight_data[flight_name]["departure_time"] = new_departure_time
            save_flight_data(flight_data)
            print("Departure time updated successfully.")
        elif admin_choice == "3":
            new_flight_details = input("Enter new flight details: ")
            flight_data[flight_name]["flight_details"] = new_flight_details
            save_flight_data(flight_data)
            print("Flight details updated successfully.")
        elif admin_choice == "4":
            flight_name = input("Enter the flight name: ")
            change_seat_layout(flight_name)
        else:
            print("Invalid choice.")
    else:
        print("Flight not found.")
while True:
    print("Aeroplane Management System")
    print("\n")
    print("\n")
    print("1. User Login")
    print("2. Admin Login")
    print("3. Quit")

    choice = input("Enter your choice: ")

    if choice == "1":
        username = user_login()
        user_menu(username)
    elif choice == "2":
        username = admin_login()
        admin_menu(username)
    elif choice == "3":
        print("Goodbye!")
        save_flight_data()
        break
    else:
        print("Invalid choice. Try again.")