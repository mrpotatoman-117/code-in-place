"""
------------------------------------------------
PROPERTY BOOKING RATE SHEET CACULATOR - RATEDESK
------------------------------------------------
"""


def main():
    main_menu()
    
    


def main_menu():
    print("Welcome to RateDesk!")
    while True:
        user_input = input("1. Create a new sheet.\n2. View History\nSelect option '1' or '2': ")
        try:
            user_input = int(user_input)
        except ValueError:
            print("Invalid Input. Try Agian")
            print()
            continue

        if user_input == 1:
           print()
           room_data = data_collection()
           #create_new_sheet()
           create_new_sheet(room_data)
           break

        elif user_input == 2:
           print()
           view_history()
           break

        else:
            print("Input invalid. Try again.")
            print()
            continue



    
def create_new_sheet():
    pass




def data_collection():
    property_name = input("What is your property's name?: ")
    currency = currency_selector()
    print()
    room_data = {}
    while True:
        room_type = input("List your room types: ")
        while True:
            base_rate = input("What is your base rate for selected room type?: ")
            try:
                base_rate = float(base_rate)
                break
            except ValueError:
                print("Input invalid. Try again.")
                print()
                continue

        room_data[room_type] = {
            "base_rate": base_rate,
            "currency": currency,
            "platforms": {},
            "weekend_markup": None
        }
        room_data[room_type]["weekend_markup"] = weekend_markup()
        add_platforms(room_data, room_type)
        print()
        while True:
            adding_room_type = input("Add another room? (yes/no): ")
            if adding_room_type == "yes":
                print()
                break
            elif adding_room_type == "no":
                print()
                break
            else:
                print("Input invalid. Try again.")
                print()
                continue
        if adding_room_type == "no":
            break
    print(room_data)


def add_platforms(room_data, room_type):
    while True:
        platform_name = input("Enter OTA platform name: ")
        while True:
            commission = input("Enter commission percentage: ")
            try:
                commission = float(commission)
                print()
                break
            except ValueError:
                print("Invalid Input. Try Agian.")
                print()
                continue

        room_data[room_type]["platforms"][platform_name] = commission
        while True:
            adding_room_type = input("Add another platform? (yes/no): ")
            if adding_room_type == "yes":
                print()
                break
            elif adding_room_type == "no":
                print()
                break
            else:
                print("Input invalid. Try again.")
                print()
                continue
        if adding_room_type == "no":
            break


def currency_selector():
    while True:
        currency = input("Select currency:\n1. USD ($)\n2. INR (₹)\n3. EUR (€)\nChoose '1', '2' or '3': ")

        try:
            currency = int(currency)
        except ValueError:
            print("Invalid input. Try again.")
            print()
            continue

        if currency == 1:
            return "$"
        elif currency == 2:
            return "₹"
        elif currency == 3:
            return "€"
        else:
            print("Invalid Input. Try again.")
            print()
            continue

def weekend_markup():
    while True:
        weekend_rate_need = input("Do you want to add weekend rates? (yes/no): ")
        if weekend_rate_need == "yes":
            while True:
                weekend_rate = input("Enter markup percentage from base rate for weekend rate: ")
                try:
                    weekend_rate = float(weekend_rate)
                    print()
                    break
                except ValueError:
                    print("Invalid input. Try again.")
                    print()
                    continue
            return weekend_rate
        elif weekend_rate_need == "no":
            print()
            return
        else:
            print("Input invalid. Try again.")
            print()
            continue

        

def view_history():
    pass


if __name__ == "__main__":
    main()
                       
