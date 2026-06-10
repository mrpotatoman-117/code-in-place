"""
------------------------------------------------
PROPERTY BOOKING RATE SHEET CALCULATOR - RATEDESK
------------------------------------------------
"""
import json #To save and load history of sheets. Learned something new here. 
import pyfiglet #For fancy project title x'D


def main():
    main_menu() #In hindsight, this is not required. But it does make it easier to add more stuff later to main_menu later. 
    

def main_menu(): #This is the main menu. Allows users to create new sheet or view history as of now.
    print("Welcome to")
    print(pyfiglet.figlet_format("RateDesk")) #YAAY Fancy text title :D
    while True: #Loop until user gives valid input
        user_input = input("1. Create a new sheet.\n2. View History\nSelect option '1' or '2': ")
        try:
            user_input = int(user_input)
        except ValueError: #Learned something new to catch invalid input that might crash the whole thing. Before this, if user entered something other than 1 or 2, the program would crash. 
            print("Invalid Input. Try Agian")
            print()
            continue

        if user_input == 1:
           print()
           property_name, room_data = data_collection() #This is where all the data collection happens. It returns the property name and room data in a dictionary format.
           #create_new_sheet() #old TO BE REMOVED
           create_new_sheet(property_name, room_data) #This is where the table is generated. 
           break

        elif user_input == 2:
           print()
           view_history() #This is where user can view history of sheets. Can select property and month to view the sheet.
           break

        else:
            print("Input invalid. Try again.") #To filter invalid inputs. 
            print()
            continue

    
def create_new_sheet(property_name, room_data): #To generate table from collected data and save to json file. 
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


def generate_table(property_name, room_data): #This is the actual function used to generate table from collected data. This is used in both creating new sheet and viewing history.
    print(f"Property: {property_name}")
    print("| Room Type | Platform | Weekday Rate | Weekend Rate |") #This is the header of the table. I know it's not the best way to create a table, but it works for now. Maybe I can use some library later to make it look better.
    print("|-----------|----------|--------------|--------------|") #This is just to create a line under the header.
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


def data_collection(): #The actual function where all the data collection happens. It collects property name, currency, room types, base rates, weekend markups and OTA platforms with their commissions. It returns the property name and room data in a dictionary format.
    property_name = input("What is your property's name?: ")
    currency = currency_selector() #Only INR, USD and EUR for now. I thought of making it a separate function because it might be useful later if I want to add more currencies or do something else with currency selection.
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


def add_platforms(room_data, room_type): #This is a separate function to add OTA platforms and their commissions for a specific room type. This is called from data_collection() function.
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
            
        
    


def currency_selector(): #This is a separate function to select currency. This is called from data_collection() function. I thought of making it a separate function because it might be useful later if I want to add more currencies or do something else with currency selection.
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

def weekend_markup(): #This is a separate function to add weekend markup for a specific room type. This is called from data_collection() function. I thought of making it a separate function because not all properties might have weekend markups, and it keeps the code cleaner.
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


def save_to_json(property_name, room_data): #This as the name suggest saves data to a json file. It checks if history exisits and if does not, creates an empty dictionary.
    while True:
        save_for_month = input("Enter month and year for which you want to save the sheet (e.g., 'January 2024'): ")
        month_confirmation = input(f"{save_for_month}. Type 'yes' to confirm or 'no' to re-enter: ")
        if month_confirmation == "yes":
            try:
                with open("history.json", "r") as f: #Learned about file handling in python to read and write json files. Before this, I was not able to save history of sheets and view them later. Now, I can save the sheets in a json file and load them later to view history.
                    history = json.load(f)
            except FileNotFoundError: #Learned something new again to handle the case when history.json does not exist. Before this, if user tried to save a sheet without any existing history, the program would crash. Now it creates an empty history if the file is not found.
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

        

def view_history(): #This is the function to view history of sheets from main menu. 
    try:
        with open("history.json", "r") as f:
            history = json.load(f)
    except FileNotFoundError:
        print("No history found.")
        return
    
    #Show properties
    print("\nSaved properties:")
    for index, property_name in enumerate(history, start=1): #Learned about enumerate function in python to loop through a list with index. Before this, I was using a regular for loop with a separate index variable, which was more cumbersome. Now I can use enumerate to get both the index and the property name in a cleaner way.
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
                       
