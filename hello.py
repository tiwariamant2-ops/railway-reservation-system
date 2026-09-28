import json
import os
import random


class RailwayReservationSystem:
    def __init__(self):
        self.db_file = "railway_data.json"
        self.data = self.load_data()

    def load_data(self):
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, "r") as file:
                    return json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                pass

        default_data = {
            "trains": {
                "12626": {"name": "Kerala Express", "route": "NDLS to TVC", "seats": 50, "fare": 750.0},
                "12952": {"name": "Mumbai Rajdhani", "route": "NDLS to BCT", "seats": 30, "fare": 2100.0},
                "12002": {"name": "Bhopal Shatabdi", "route": "NDLS to RKMP", "seats": 40, "fare": 1200.0},
            },
            "bookings": {},
        }
        self.save_data(default_data)
        return default_data

    def save_data(self, data=None):
        if data is None:
            data = self.data
        with open(self.db_file, "w") as file:
            json.dump(data, file, indent=4)

    def view_trains(self):
        print("\n" + "=" * 60 + "\n AVAILABLE TRAINS & ROUTE SCHEDULE \n" + "=" * 60)
        print(f"{'Train No':<10} | {'Train Name':<20} | {'Route':<15} | {'Seats':<6} | {'Fare'}")
        print("-" * 65)
        for t_no, info in self.data["trains"].items():
            print(f"{t_no:<10} | {info['name']:<20} | {info['route']:<15} | {str(info['seats']):<6} | ₹{info['fare']}")
        print("=" * 60)

    def book_ticket(self):
        print("\n--- Book Train Ticket ---")
        self.view_trains()
        train_no = input("Enter 5-Digit Train Number: ").strip()
        if train_no not in self.data["trains"]:
            print("❌ Error: Invalid Train Number!")
            return

        train = self.data["trains"][train_no]
        if train["seats"] <= 0:
            print("Transaction Failed: No seats available in this train!")
            return

        passenger_name = input("Enter Passenger Full Name: ").strip()
        if not passenger_name:
            print("Error: Passenger name cannot be empty!")
            return

        try:
            passenger_age = int(input("Enter Passenger Age: "))
            if passenger_age <= 0 or passenger_age > 120:
                raise ValueError
        except ValueError:
            print("❌ Error: Invalid age entered!")
            return

        pnr = f"PNR{random.randint(100000, 999999)}"
        train["seats"] -= 1
        self.data["bookings"][pnr] = {
            "train_no": train_no,
            "train_name": train["name"],
            "route": train["route"],
            "passenger": passenger_name,
            "age": passenger_age,
            "fare_paid": train["fare"],
            "status": "Confirmed",
        }
        self.save_data()
        print("\n" + "=" * 15)
        print(f"TICKET BOOKED SUCCESSFULLY!\n📌 YOUR PNR NUMBER: {pnr}\n💰 Fare Deducted: ₹{train['fare']:.2f}")
        print("=" * 15)

    def check_pnr_status(self):
        print("\n--- Check PNR Status ---")
        pnr = input("Enter your PNR Number: ").strip().upper()
        if pnr not in self.data["bookings"]:
            print("Error: No reservation record found for this PNR.")
            return

        ticket = self.data["bookings"][pnr]
        print("\n==========================================")
        print(f" RESERVATION DETAILS FOR PNR: {pnr}")
        print("==========================================")
        print(f"Passenger Name : {ticket['passenger']}")
        print(f"Passenger Age  : {ticket['age']}")
        print(f"Train Number   : {ticket['train_no']}")
        print(f"Train Name     : {ticket['train_name']}")
        print(f"Route          : {ticket['route']}")
        print(f"Fare paid      : ₹{ticket['fare_paid']}")
        print(f"Status         : {ticket['status']}")
        print("------------------------")

    def cancel_ticket(self):
        print("\n--- Cancel Train Reservation ---")
        pnr = input("Enter your PNR Number to cancel: ").strip().upper()
        if pnr not in self.data["bookings"]:
            print("❌ Error: Invalid PNR Number!")
            return

        ticket = self.data["bookings"][pnr]
        if ticket["status"] == "Cancelled":
            print("This ticket is already cancelled.")
            return

        train_no = ticket["train_no"]
        self.data["trains"][train_no]["seats"] += 1
        ticket["status"] = "Cancelled"
        self.save_data()
        print(f"Ticket associated with PNR {pnr} has been successfully cancelled. Refund processed!")

    def menu(self):
        while True:
            print("\n" + "═" * 40 + "\n INDIAN RAILWAYS CLI SYSTEM \n" + "═" * 40)
            print("1. View Available Trains & Seats\n2. Book Train Ticket\n3. Check PNR Status\n4. Cancel Ticket\n5. Exit System")
            print("═" * 40)
            choice = input("Select an option (1-5): ").strip()

            if choice == '1':
                self.view_trains()
            elif choice == '2':
                self.book_ticket()
            elif choice == '3':
                self.check_pnr_status()
            elif choice == '4':
                self.cancel_ticket()
            elif choice == '5':
                print("\nThank you for traveling with Indian Railways. Goodbye!")
                break
            else:
                print("Invalid Choice! Please enter a number between 1 and 5.")


if __name__ == "__main__":
    railway = RailwayReservationSystem()
    railway.menu()


                                 

                    


                


                        
    
          
                   
            
        


         

    
