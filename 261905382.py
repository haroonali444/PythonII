# Variable constant for data file
FLIGHTS_DATA_FILE = "flights_data.txt"

# Store flight data
flights = {}

#Loading flight data from file
def load_flights_data():
    if not file_exists(FLIGHTS_DATA_FILE):
        print(f"File '{FLIGHTS_DATA_FILE}' not found. Initializing empty flight data.")
        return

    with open(FLIGHTS_DATA_FILE, "r") as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split(': ')
            flight_name = parts[0]
            flight_details = parts[1]
            flights[flight_name] = {
                'company': flight_details,
                'seats': []  # Add an empty list for seats
            }

#checking if a file exists
def file_exists(file_path):
    try:
        with open(file_path, "r"):
            return True
    except FileNotFoundError:
        return False

#Saving flight data to the file
def save_flights_data():
    with open(FLIGHTS_DATA_FILE, "w") as file:
        for flight_name, flight in flights.items():
            file.write(f"{flight_name}: {flight['company']}\n")

# Initialize flight data
load_flights_data()

# display seat availability for a specific flight
def display_seat_availability(flight_name):
    flight = flights.get(flight_name)
    if flight:
        print(f"Seat Availability for {flight['company']}:")
        for row_num, row in enumerate(flight['seats'], start=1):
            print(f"Row {row_num}:", " ".join(row))
    else:
        print("Flight not found.")
#book a seat for a passenger on a specific flight.
def book_seat(flight_name):

    flight = flights.get(flight_name)
    if flight:
        row = int(input("Enter the row number: ")) - 1
        seat_num = input("Enter the seat number (A-F): ").upper()

        valid_seat_letters = ['A', 'B', 'C', 'D', 'E', 'F']

        #check if the row and seat inputs are valid
        if 0 <= row < len(flight['seats']) and seat_num in valid_seat_letters:
            seat_index = valid_seat_letters.index(seat_num)
            if flight['seats'][row][seat_index] == '*':
                flight['seats'][row][seat_index] = 'X'
                print("Seat booked successfully.")
                save_booking_confirmation(flight_name, row, seat_num)
            else:
                print("Seat already booked.")
        else:
            print("Invalid input. Please try again.")
    else:
        print("Flight not found.")


def save_booking_confirmation(flight_name, row, seat_num):
    #opennig the booking confirmation file in append mode
    with open(f"{flight_name}_bookings.txt", "a") as file:
        file.write(f"Row {row+1}{seat_num} - {flights[flight_name]['company']}\n")

def cancel_booking(flight_name):
    # Get the flight data from the 'flights' dictionary
    flight = flights.get(flight_name)

    # Check if the flight exists
    if flight:

        row = int(input("Enter the row number to cancel: ")) - 1
        seat_num = input("Enter the seat number (A-F) to cancel: ").upper()

        if 0 <= row < len(flight['seats']) and seat_num in 'ABCDEF':
            # Check if the seat is already booked ('X')
            if flight['seats'][row].count('X') > 0:
                seat_index = flight['seats'][row].index('X')
                flight['seats'][row][seat_index] = '*'
                print("Booking canceled successfully.")
                # Remove the booking confirmation from the file
                remove_booking_confirmation(flight_name, row, seat_num)
            else:
                print("Seat is not booked.")
        else:
            print("Invalid input. Please try again.")
    else:
        print("Flight not found.")

def remove_booking_confirmation(flight_name, row, seat_num):
    confirmation_file_path = f"{flight_name}_bookings.txt"
    
    # Check if the confirmation file exists before attempting to read it
    try:
        with open(confirmation_file_path, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Booking confirmation file for {flight_name} does not exist.")
        return

    # Open the confirmation file in "write" mode to overwrite its content
    with open(confirmation_file_path, "w") as file:
        for line in lines:
            if f"Row {row+1}{seat_num} - {flights[flight_name]['company']}\n" != line:
                file.write(line)


def show_flights():
    print("List of available flights:")
    #iterate through the flights dictionary to display each flight
    for flight_name, flight in flights.items():
        print(f"Flight Company: {flight['company']}")
        display_seat_availability(flight_name)
        print()

def admin_login():
    #authenticate the admin with a username and password
    admin_username = "admin123"  # Change this to your desired admin username
    admin_password = "adminpassword123"  # Change this to your desired admin password

    entered_username = input("Enter admin username: ")
    entered_password = input("Enter admin password: ")

    if entered_username == admin_username and entered_password == admin_password:
        print("Admin login successful!")
        admin_interface()
    else:
        print("Incorrect admin credentials. Please try again.")

def admin_interface():
    #provide options for the admin to manage flight details
    while True:
        print("Admin Interface")
        print("1. Manage Flight Details")
        print("2. Quit")

        admin_choice = input("Enter your choice: ")

        if admin_choice == '1':
            manage_flight_details()
        elif admin_choice == '2':
            print("Exiting admin interface.")
            break

def manage_flight_details():
    #allow the admin to modify flight details
    print("Flights available for modification:")
    for flight_name, flight in flights.items():
        print(f"{flight_name}: {flight['company']}")

    flight_to_modify = input("Select a flight to modify: ")
    if flight_to_modify in flights:
        flight = flights[flight_to_modify]
        print(f"Flight Details for {flight['company']}:")
        print("1. Change Arrival Time")
        print("2. Change Departure Time")
        print("3. Change Flight Details")
        print("4. Change Seat Layout")
        print("5. Go Back")

        choice = input("Enter your choice: ")

        if choice == '1':
            new_arrival_time = input("Enter new arrival time: ")
            flight['arrival_time'] = new_arrival_time
            print("Arrival time updated successfully.")
        elif choice == '2':
            new_departure_time = input("Enter new departure time: ")
            flight['departure_time'] = new_departure_time
            print("Departure time updated successfully.")
        elif choice == '3':
            new_flight_details = input("Enter new flight details: ")
            flight['details'] = new_flight_details
            print("Flight details updated successfully.")
        elif choice == '4':
            new_seat_layout = input("Enter new seat layout: ")
            flight['seats'] = [[seat for seat in row] for row in new_seat_layout.split()]
            print("Seat layout updated successfully.")
        elif choice == '5':
            print("Going back to the admin interface.")
        else:
            print("Invalid choice. Please try again.")
    else:
        print("Flight not found.")
#main function for the system
def main():
    load_flights_data()

    while True:
        print("Airplane Management System [Assignment 01]")
        print("1. User Functions")
        print("2. Admin Interface")
        print("3. Quit")

        choice = input("Enter your choice: ")

        if choice == '1':
            print("Welcome to the User Interface")
            print("1. Booking a Ticket")
            print("2. Display Seat Availability")
            print("3. Book a Seat")
            print("4. Cancel a Booking")
            print("5. Show Flights")
            print("6. Go Back")

            user_choice = input("Enter your choice: ")

            if user_choice == '1':
                print("Available flights:")
                for flight_name in flights.keys():
                    print(f"{flight_name}: {flights[flight_name]['company']}")
                selected_flight = input("Select a flight to book: ")
                book_seat(selected_flight)
            elif user_choice == '2':
                selected_flight = input("Enter flight name to display seat availability: ")
                display_seat_availability(selected_flight)
            elif user_choice == '3':
                selected_flight = input("Enter flight name to book a seat: ")
                book_seat(selected_flight)
            elif user_choice == '4':
                selected_flight = input("Enter flight name to cancel a booking: ")
                cancel_booking(selected_flight)
            elif user_choice == '5':
                show_flights()
            elif user_choice == '6':
                print("Going back to the main menu.")
            else:
                print("Invalid choice. Please try again.")
        elif choice == '2':
            admin_login()
        elif choice == '3':
            save_flights_data()
            print("Exiting the system.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    #it starts the flight management system
    main()
