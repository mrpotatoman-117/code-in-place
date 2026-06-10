"""
------------------------------------------------
PROPERTY BOOKING RATE SHEET CACULATOR - RATEDESK
------------------------------------------------
"""
import json
import pyfiglet


def main():
    main_menu()
    
    


def main_menu():
    print("Welcome to")
    print(pyfiglet.figlet_format("RateDesk"))
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
           property_name, room_data = data_collection()
           #create_new_sheet() #old TO BE REMOVED
           create_new_sheet(property_name, room_data)
           break

        elif user_input == 2:
           print()
           view_history()
           break

        else:
            print("Input invalid. Try again.")
            print()
            continue

    
def create_new_sheet(property_name, room_data):
    generate_table(property_name, room_data)
    while True:
        save_data = input("Do you want to save this sheet? (yes/no): ")
        if save_data == "yes":
            break
        elif save_data == "no":
            print("Sheet not saved.")
            return
        else:
            print("Input invalid. Try again.")
            print()
            continue
    save_to_json(property_name, room_data)

"""
### ALL CALCULATION MOVDED TO generate_table() ###

    for room_type, room_info in room_data.items():
        base_rate = room_info["base_rate"]
        weekend_markup = room_info["weekend_markup"]
        
        if room_info["platforms"]:  #platforms exist
            for platform, commission in room_info["platforms"].items():
                weekday_rate = base_rate * (1 + commission/100)
                if weekend_markup is not None:
                    weekend_rate = base_rate * (1 + weekend_markup/100) * (1 + commission/100)
                else:
                    weekend_rate = None
                print(f"Room: {room_type}, Platform: {platform}, Weekday: {room_info['currency']}{weekday_rate:.2f}", end="")
                if weekend_rate is not None:
                    print(f", Weekend: {room_info['currency']}{weekend_rate:.2f}")
                else:
                    print(", Weekend: N/A")
        
        else:  #no platforms
            print(f"Room: {room_type}, Base Rate: {room_info['currency']}{base_rate:.2f}, No platforms added")
"""

def generate_table(property_name, room_data):
    print(f"Property: {property_name}")
    print("| Room Type | Platform | Weekday Rate | Weekend Rate |")
    print("|-----------|----------|--------------|--------------|")
    for room_type, room_info in room_data.items():
        base_rate = room_info["base_rate"]
        weekend_markup = room_info["weekend_markup"]
        
        if room_info["platforms"]:  #platforms exist
            for platform, commission in room_info["platforms"].items():
                weekday_rate = base_rate * (1 + commission/100)
                if weekend_markup is not None:
                    weekend_rate = base_rate * (1 + weekend_markup/100) * (1 + commission/100)
                else:
                    weekend_rate = None
                print(f"| {room_type} | {platform} | {room_info['currency']}{weekday_rate:.2f} | ", end="")
                if weekend_rate is not None:
                    print(f"{room_info['currency']}{weekend_rate:.2f} |")
                else:
                    print("N/A |")
        
        else:  #no platforms
            print(f"| {room_type} | N/A | {room_info['currency']}{base_rate:.2f} | N/A |")


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
    return property_name, room_data


def add_platforms(room_data, room_type):
    ota_platform_need = input("Do you want to add OTA platforms for this room type? (yes/no): ")
    if ota_platform_need == "yes":
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
    else:
        print()
        return
            
        
    


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


def save_to_json(property_name, room_data):
    while True:
        save_for_month = input("Enter month and year for which you want to save the sheet (e.g., 'January 2024'): ")
        month_confirmation = input(f"{save_for_month}. Type 'yes' to confirm or 'no' to re-enter: ")
        if month_confirmation == "yes":
            try:
                with open("history.json", "r") as f:
                    history = json.load(f)
            except FileNotFoundError:
                history = {}

            if property_name not in history:
                history[property_name] = {}
            history[property_name][save_for_month] = room_data

            with open("history.json", "w") as f:
                json.dump(history, f)
            
            print("Sheet saved successfully!")
            break

        elif month_confirmation == "no":
            print()
            continue

        else:
            print("Input invalid. Try again.")
            print()
            continue

        

def view_history():
    try:
        with open("history.json", "r") as f:
            history = json.load(f)
    except FileNotFoundError:
        print("No history found.")
        return
    
    #Show properties
    print("\nSaved properties:")
    for index, property_name in enumerate(history, start=1):
        print(f"{index}. {property_name}")

    while True:
        try:
            choice = int(input("\nSelect a property: "))
            if 1 <= choice <= len(history):
                break
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Invalid input. Try again.")
    
    selected_property = list(history.keys())[choice - 1]

    #Show months
    print(f"\nSaved months for {selected_property}:")
    for index, month in enumerate(history[selected_property], start=1):
        print(f"{index}. {month}")

    while True:
        try:
            choice = int(input("\nSelect a month: "))
            if 1 <= choice <= len(history[selected_property]):
                break
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Invalid input. Try again.")

    selected_month = list(history[selected_property].keys())[choice - 1]

    #Display table
    room_data = history[selected_property][selected_month]
    print()
    generate_table(selected_property, room_data)




if __name__ == "__main__":
    main()
                       
