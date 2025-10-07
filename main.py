import os
import random
import time

# Hello, my name is Camila Rose, and I am the creator of this game
# called Py.City

# For context, I really enjoy tycoon/management games — what I jokingly call
# the "boring" genre.

# This game, as you can tell by the title, is heavily inspired by Maxis / EA's
# SimCity.

# Below is a small guide about the general function of each part of the code.

# ================================================================================

# Global game data

# Fun fact: to build this prototype I wanted to try some concepts beyond what
# we covered in Code in Place, which took me some time to research.

# For all game functions, roughly 23 global variables were defined (mostly empty)
# to ensure they are editable at runtime.

city = ""
mayor = ""
funds = 75_000_000
citizens_count = 1000
zones = {
    "residential": 1,
    "commercial": 1,
    "industrial": 1
}
day = 1
taxes = {
    "residential": 5,
    "commercial": 5,
    "industrial": 5
}
sectors = {"Old Town": {"residential": 1, "commercial": 1, "industrial": 1}}
transport_routes = []
citizens_info = []
zone_wear = {"residential": 0, "commercial": 0, "industrial": 0}
elections_every_days = 30
days_to_elections = elections_every_days
citizen_satisfaction = 75
achievements = []
newspaper_headlines = []
current_weather = "Sunny"

population_history = [citizens_count]
funds_history = [funds]
satisfaction_history = [citizen_satisfaction]

special_zones_available = {
    "national park": {"cost": 20_000_000, "population_requirement": 5000, "unlocked": False, "satisfaction_impact": 10},
    "technology hub": {"cost": 30_000_000, "population_requirement": 7000, "unlocked": False, "funds_impact": 5_000_000},
    "airport": {"cost": 50_000_000, "population_requirement": 10000, "unlocked": False, "funds_impact": 10_000_000},
    "university": {"cost": 40_000_000, "population_requirement": 8000, "unlocked": False, "citizens_impact": 500}
}
special_zones_built = []

advisors = {
    "economic": "Economic Advisor: 'Your funds are running low; consider raising taxes or seeking new investments.'",
    "environmental": "Environmental Advisor: 'Pollution in industrial zones is rising; maybe time to invest in clean tech?'",
    "popularity": "Popularity Advisor: 'Citizens are unhappy with taxes. You could lower them to improve your approval.'"
}


# Clears the terminal for a clean gameplay flow.
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# This is the game's title, drawn in ASCII art.
def ascii_title():
    print(r"""            
▀██▀▀█▄                   ▄▄█▀▀▀▄█  ██    ▄                   
 ██   ██  ▄▄▄▄ ▄▄▄      ▄█▀     ▀  ▄▄▄  ▄██▄   ▄▄▄▄ ▄▄▄     
 ██▄▄▄█▀   ▀█▄  █       ██          ██   ██     ▀█▄  █      
 ██         ▀█▄█        ▀█▄      ▄  ██   ██      ▀█▄█       
▄██▄         ▀█          ▀▀█▄▄▄▄▀  ▄██▄  ▀█▄▀     ▀█        
          ▄▄ █      ██                         ▄▄ █         
           ▀▀                                   ▀▀          
    """)
    print("       Welcome to Py.City! By Camila Rose.\n")

# Now that we have the title and some variables defined, let's define the
# functions that will be used during gameplay.

# ===== GAME FUNCTIONS =====

# Main menu definition. This runs first when the program is executed.
def main_menu():
    while True:
        clear_screen()
        ascii_title()
        print("1. Play")
        print("2. Quit")
        option = input("Choose an option: ")
        if option == '1':
            setup_game()
            break
        elif option == '2':
            exit()
        else:
            input("Invalid option. Press Enter to continue...")

# Game setup: choose a name for your city and your mayor.
def setup_game():
    global city, mayor, citizens_info
    clear_screen()
    city = input("Enter the name of your city: ")
    mayor = input("Enter the name of the mayor: ")

    # Based on the list of citizens defined in generate_citizen, create
    # random citizens and assign social class. This affects reactions to taxes
    # and happiness.
    for _ in range(citizens_count):
        citizens_info.append(generate_citizen())
    show_initial_newspaper()
    tutorial()
    game_loop()

# Generate a citizen with random name, satisfaction, and social class.
def generate_citizen():
    names = ["Anna", "Louis", "Sophia", "Charles", "Mary", "Peter", "Ellen", "Joseph"]
    social_classes = ["Low", "Middle", "High"]
    return {
        "name": random.choice(names),
        "satisfaction": random.randint(50, 100),
        "social_class": random.choice(social_classes)
    }

def update_citizen_satisfaction():
    global citizen_satisfaction
    total_satisfaction = sum(c["satisfaction"] for c in citizens_info)
    citizen_satisfaction = total_satisfaction / len(citizens_info) if len(citizens_info) > 0 else 0

# Show the initial newspaper announcing your election as mayor.
def show_initial_newspaper():
    clear_screen()
    print(f"""
   _________________________________
  |                                 |
  |         PY.CITY GAZETTE         |
  |_________________________________|
  |                                 |
  | {mayor} elected as the new mayor |
  | of {city}!                       |
  |                                 |
  |  As the new mayor, you should   |
  |  know that if you raise taxes   |
  |  too much or neglect the city,  |
  |  citizens will get upset.        |  
  |                                 |
  |  How much will {city} grow      |
  |  under {mayor}'s leadership?    |
  |                                 |
  |  We'll see how you do in the    |
  |  upcoming elections!             |
  |_________________________________|
    """)
    input("\nPress Enter to continue...")

# Daily newspaper printed at the end of the day summarizing the day's events.
def show_daily_newspaper():
    clear_screen()
    print(f"📰 === {city.upper()} GAZETTE === 📰")
    print(f"Date: Day {day}")
    print("-" * 30)
    if not newspaper_headlines:
        print("No major news today.")
    else:
        for headline in newspaper_headlines:
            print(f"📰 | {headline}")
    print("-" * 30)
    newspaper_headlines.clear()
    input("\nPress Enter to continue...")


def tutorial():
    clear_screen()
    print("========== ASSISTANT ==========")
    print(f"\nMayor {mayor}, I have a few things I think you should know!")
    print(f"\n\n{city} is a beautiful and prosperous city, but if you want to earn money,\nconsider raising taxes and creating new zones. Don't forget citizen\nhappiness: maintain services and zones, and consider building a public\ntransportation system.")
    input("\nPress Enter to continue...")

# Game menu (prints the current status and options; used on each loop iteration).
def game_menu():
    print(f"\nDay: {day} | City: {city} | Mayor: {mayor} | Weather: {current_weather}")
    print(f"Citizen satisfaction: {citizen_satisfaction:.2f}%")
    print(f"Days until elections: {days_to_elections}")

    print("\n==== MANAGEMENT ====")
    print("1. View funds menu")
    print("2. Manage taxes")
    print("3. Build a zone")
    print("4. Manage services")
    print("5. View city")
    print("6. Advance day")
    print("7. Create sector")
    print("8. Manage public transportation")

    print("\n==== DATA ====")
    print("9. View growth charts")
    print("10. View achievements")
    print("11. Advisor tips")
    print("12. Build special zone")
    print("13. Quit")


# ===== SECTIONS / MENUS =====

def view_funds():
    clear_screen()
    print(f"\nFunds: ${funds:,}")
    print(f"Citizens: {len(citizens_info)}")
    print("\nZone wear:")
    for z, lvl in zone_wear.items():
        print(f"{z.capitalize()}: {lvl}%")
    input("\nPress Enter to return...")

def manage_policies():
    clear_screen()
    global taxes, citizen_satisfaction
    print("\nCurrent tax rates:")
    for z, rate in taxes.items():
        print(f"{z.capitalize()}: {rate}%")

    zone_choice = input("\nWhich zone do you want to change the tax for? (residential, commercial, industrial): ").lower()
    if zone_choice in taxes:
        try:
            new_rate = int(input("New rate (%): "))
            if new_rate < 0:
                print("Tax rate cannot be negative.")
                input("\nPress Enter to continue...")
                return
            
            difference = new_rate - taxes[zone_choice]
            taxes[zone_choice] = new_rate
            print(f"Tax rate for {zone_choice} changed to {new_rate}%")

            # Affect citizen satisfaction according to tax changes
            if difference > 0:  # Tax increase
                for citizen in citizens_info:
                    if citizen["social_class"] == "Low":
                        citizen["satisfaction"] -= (difference * 1.5)  # Bigger impact on low class
                    elif citizen["social_class"] == "Middle":
                        citizen["satisfaction"] -= (difference * 1)
                    else:
                        citizen["satisfaction"] -= (difference * 0.5)
                newspaper_headlines.append(f"Protests over high taxes in {zone_choice} zones!")
                print("Citizens are unhappy about the tax increase.")
            elif difference < 0:  # Tax decrease
                for citizen in citizens_info:
                    if citizen["social_class"] == "Low":
                        citizen["satisfaction"] += (abs(difference) * 1.5)
                    elif citizen["social_class"] == "Middle":
                        citizen["satisfaction"] += (abs(difference) * 1)
                    else:
                        citizen["satisfaction"] += (abs(difference) * 0.5)
                newspaper_headlines.append(f"Relief as taxes drop in {zone_choice} zones.")
                print("Citizens appreciate the tax decrease.")

            update_citizen_satisfaction()

        except ValueError:
            print("Invalid value. Please enter an integer.")
    else:
        print("Invalid zone.")
    input("\nPress Enter to continue...")

def manage_services():
    clear_screen()
    global funds, citizen_satisfaction, newspaper_headlines
    print("\n1. Improve water service ($2,000,000)")
    print("2. Improve electricity ($2,000,000)")
    print("3. Create public transportation ($15,000,000)")
    print("4. General maintenance for zones ($5,000,000)")
    option = input("Select an option: ")

    improvements = {"1": 2_000_000, "2": 2_000_000, "3": 15_000_000, "4": 5_000_000}

    if option in improvements:
        cost = improvements[option]
        if funds >= cost:
            funds -= cost
            if option == '1':
                print("Water service improved.")
                citizen_satisfaction = min(100, citizen_satisfaction + 5)
                newspaper_headlines.append("Water service has greatly improved.")
            elif option == '2':
                print("Electricity service improved.")
                citizen_satisfaction = min(100, citizen_satisfaction + 5)
                newspaper_headlines.append("Greater reliability in electricity supply.")
            elif option == '3':
                print("You can now create public transport routes from the main menu.")
                newspaper_headlines.append("Public transportation initiative launched!")
            elif option == '4':
                print("General maintenance performed across all zones.")
                for z in zone_wear:
                    zone_wear[z] = max(0, zone_wear[z] - 20)  # Reduce wear
                newspaper_headlines.append("City-wide maintenance works completed.")
                print("Zone wear has decreased.")
            print("Service improved.")
        else:
            print("You do not have enough funds.")
    else:
        print("Invalid option.")
    input("\nPress Enter to continue...")

def view_city():
    clear_screen()
    print("\nCurrent state of your city by sectors:\n")
    if not sectors:
        print("No sectors created yet.")
        input("\nPress Enter to continue...")
        return

    for sector_name, sector_zones in sectors.items():
        print(f"--- Sector: {sector_name} ---")
        if sum(sector_zones.values()) == 0:
            print("  This sector has no built zones yet.")
        else:
            for i in range(sector_zones["residential"]):
                print("\033[92m[R]\033[0m", end=" ")
            for i in range(sector_zones["commercial"]):
                print("\033[94m[C]\033[0m", end=" ")
            for i in range(sector_zones["industrial"]):
                print("\033[93m[I]\033[0m", end=" ")
            print()  # New line after each sector
        print("-" * (len(f"--- Sector: {sector_name} ---")))

    print("\n\nLegend: [R]=Residential, [C]=Commercial, [I]=Industrial")
    
    if special_zones_built:
        print("\nSpecial zones built:")
        for sz in special_zones_built:
            print(f"- {sz.capitalize()}")

    input("\nPress Enter to continue...")

def advance_day():
    clear_screen()
    global day, funds, citizens_count, days_to_elections, citizen_satisfaction, newspaper_headlines, current_weather
    
    clear_screen()
    print("Advancing a day...")
    time.sleep(1)  # Small pause to simulate time passing

    day += 1
    days_to_elections -= 1

    # Calculate tax revenue
    revenue = 0
    for z in zones:
        revenue += taxes[z] * zones[z] * 10_000
    
    # Impact of wear on funds
    wear_cost = 0
    for z, lvl in zone_wear.items():
        if lvl > 50:  # If wear is high, generate a maintenance cost
            wear_cost += lvl * 1000  # Larger cost the more wear
            newspaper_headlines.append(f"Issues in the {z} zone due to lack of maintenance.")
            print(f"Zone {z} reports contamination/infrastructure problems.")
            for c in citizens_info:  # Reduce satisfaction due to degraded zones
                c["satisfaction"] -= (lvl / 10)
    funds -= wear_cost

    # Affect citizens and funds based on taxes and city conditions
    for citizen in citizens_info:
        # Citizens with low satisfaction might migrate
        if citizen["satisfaction"] < 30 and random.random() < 0.1:  # 10% chance to migrate
            print(f"{citizen['name']} has migrated due to low satisfaction.")
            citizens_info.remove(citizen)
            newspaper_headlines.append(f"{citizen['name']} leaves the city due to discontent.")
            break  # Exit the loop to avoid list modification errors

    # Population increase/decrease
    citizens_change = random.randint(-10, 50)
    if citizen_satisfaction < 50:
        citizens_change -= 20  # Low satisfaction makes population more likely to drop
    elif citizen_satisfaction > 80:
        citizens_change += 30  # High satisfaction increases population growth chance

    # Ensure no negative citizens
    if len(citizens_info) + citizens_change < 0:
        citizens_change = -len(citizens_info)

    for _ in range(abs(citizens_change)):
        if citizens_change > 0:
            citizens_info.append(generate_citizen())
        else:
            if len(citizens_info) > 0:
                citizens_info.pop(random.randint(0, len(citizens_info) - 1))

    citizens_count = len(citizens_info)  # Update global citizens count
    funds += revenue

    # Increase zone wear
    for z in zone_wear:
        zone_wear[z] += random.randint(1, 5)  # Wear increases each day

    # Random weather
    weathers = ["Sunny", "Rainy", "Cloudy", "Snowy", "Storm"]
    previous_weather = current_weather
    current_weather = random.choice(weathers)
    if current_weather != previous_weather:
        newspaper_headlines.append(f"Weather change: Today it's {current_weather}.")
    
    if current_weather == "Snowy":
        print("Snow! Public transportation may be slower and maintenance costs increase.")
        funds -= 1_000_000  # Extra cost for snow
        for c in citizens_info:
            c["satisfaction"] -= 2  # Slight satisfaction drop
    elif current_weather == "Storm":
        print("Electrical storm! Possible power outages and minor damages.")
        funds -= 2_000_000  # Extra cost for storm
        for c in citizens_info:
            c["satisfaction"] -= 5  # Satisfaction drop
        if random.random() < 0.2:  # 20% chance of damage
            affected_zone = random.choice(list(zone_wear.keys()))
            zone_wear[affected_zone] += 10
            newspaper_headlines.append(f"Damage in the {affected_zone} zone due to storm.")
    
    update_citizen_satisfaction()

    random_event()
    check_achievements()  # Check achievements when advancing the day
    bankruptcy()

    # History for charts
    population_history.append(len(citizens_info))
    funds_history.append(funds)
    satisfaction_history.append(citizen_satisfaction)

    if days_to_elections <= 0:
        elections()

def bankruptcy():
    clear_screen()
    global funds
    if funds <= -5_000_000:
        print("You have gone bankrupt!")
        print("GAME OVER.")
        input("Press Enter to exit...")
        exit()

def create_sector():
    clear_screen()
    print("\nCREATE NEW SECTOR")
    name = input("Sector name: ")
    if name.strip() == "":
        print("Sector name cannot be empty.")
        input("Press Enter to continue...")
        return
    if name in sectors:
        print("That sector already exists.")
        input("Press Enter to continue...")
        return
    sectors[name] = {"residential": 0, "commercial": 0, "industrial": 0}
    print(f"The sector '{name}' has been successfully created.")
    newspaper_headlines.append(f"A new sector has been founded: '{name}'!")
    input("\nPress Enter to continue...")

def build_zone_with_sectors():
    clear_screen()
    print("\nAVAILABLE SECTORS:")
    if not sectors:
        print("No sectors created yet. Create one first.")
        input("Press Enter to continue...")
        return

    for s in sectors:
        print(f"- {s}")
    sector = input("In which sector do you want to build? (type the exact name): ")
    if sector not in sectors:
        print("Invalid sector.")
        input("Press Enter to continue...")
        return

    print("\n1. Build residential zone ($5,000,000)")
    print("2. Build commercial zone ($7,000,000)")
    print("3. Build industrial zone ($10,000,000)")
    choice = input("Select an option: ")

    costs = {"1": ("residential", 5_000_000),
             "2": ("commercial", 7_000_000),
             "3": ("industrial", 10_000_000)}

    if choice in costs:
        zone_type, cost = costs[choice]
        global funds
        if funds >= cost:
            funds -= cost
            sectors[sector][zone_type] += 1
            if zone_type in zones:  # Ensure the global 'zones' is also updated for taxes
                zones[zone_type] += 1
            else:
                zones[zone_type] = 1
            print(f"{zone_type.capitalize()} zone successfully built in {sector}.")
            newspaper_headlines.append(f"New {zone_type} zone built in sector '{sector}'.")
        else:
            print("You do not have enough funds.")
    else:
        print("Invalid option.")
    input("\nPress Enter to continue...")

def manage_public_transport():
    clear_screen()
    global funds, transport_routes, newspaper_headlines
    print("\nCREATE NEW PUBLIC TRANSPORT ROUTE")
    transport_type = input("What type of transport is it? (Bus, Tram, Metro, etc.): ")
    route_name = input("Route name: ")
    print("Current sectors:")
    for s in sectors:
        print(f"- {s}")
    route = input("Type the sectors separated by commas that the route will cover: ")
    sector_list = [s.strip() for s in route.split(",") if s.strip() in sectors]
    
    if not sector_list:
        print("No valid sectors entered or the sectors do not exist.")
        input("Press Enter to continue...")
        return

    cost = 15_000_000
    if funds >= cost:
        funds -= cost
        transport_routes.append({"type": transport_type, "name": route_name, "sectors": sector_list})
        print(f"Route '{route_name}' of type {transport_type} successfully created, covering: {', '.join(sector_list)}.")
        newspaper_headlines.append(f"The new {transport_type} route '{route_name}' is inaugurated!")
        for citizen in citizens_info:  # Increase satisfaction due to new transport
            citizen["satisfaction"] += random.randint(3, 8)
        update_citizen_satisfaction()
    else:
        print("You do not have enough funds.")
    input("\nPress Enter to continue...")

def random_event():
    global funds, citizens_info, newspaper_headlines
    events = [
        ("An earthquake shakes the city!", -random.randint(5_000_000, 10_000_000), "earthquake"),
        ("A foreign investment arrives!", random.randint(10_000_000, 20_000_000), "investment"),
        ("Protests over high taxes!", -random.randint(2_000_000, 5_000_000), "protests"),
        ("A new park is inaugurated!", -1_000_000, "park"),
        ("An economic fair boosts businesses!", random.randint(5_000_000, 8_000_000), "fair"),
        # Random mission/challenge
        ("A tech company wants to open a plant in your city.",
         lambda: ask_mission_decision("tech_company"), "mission")
    ]

    # Rare Kaiju event
    if random.randint(1, 100) == 1:
        loss = int(funds * 0.9)
        funds -= loss
        print("\n🦖 A KAIJU ATTACKS THE CITY! Chaos reigns and repairs cost a fortune!")
        print(f"You lost ${loss:,} in damages.")
        newspaper_headlines.append("KAIJU ATTACK! City in ruins and massive losses!")
        for c in citizens_info:
            c["satisfaction"] = max(0, c["satisfaction"] - 30)  # Large satisfaction drop
        update_citizen_satisfaction()
        input("\nPress Enter to continue...")
        return
    
    event_text, change, event_type = random.choice(events)

    if event_type == "mission":
        change()  # Execute the mission function
    else:
        funds += change
        print(f"\nEVENT: {event_text}")
        print(f"Impact on funds: {'+' if change >= 0 else ''}${change:,}")
        newspaper_headlines.append(event_text)  # Add to headlines

        # Impact on satisfaction depending on event
        if event_type == "earthquake":
            for c in citizens_info: c["satisfaction"] = max(0, c["satisfaction"] - 15)
        elif event_type == "investment":
            for c in citizens_info: c["satisfaction"] = min(100, c["satisfaction"] + 10)
        elif event_type == "protests":
            for c in citizens_info: c["satisfaction"] = max(0, c["satisfaction"] - 10)
        elif event_type == "park":
            for c in citizens_info: c["satisfaction"] = min(100, c["satisfaction"] + 8)
        elif event_type == "fair":
            for c in citizens_info: c["satisfaction"] = min(100, c["satisfaction"] + 5)
        
        update_citizen_satisfaction()
        input("\nPress Enter to continue...")

def ask_mission_decision(mission_id):
    global funds, citizen_satisfaction, newspaper_headlines
    if mission_id == "tech_company":
        clear_screen()
        print("MISSION: TECHNOLOGY OPPORTUNITY")
        print("A large tech company wants to build a plant in your city.")
        print("Options:")
        print("1. Accept: Gain $10,000,000, but pollution will increase and satisfaction will drop (risk of -10 satisfaction points).")
        print("2. Reject: No significant change to funds or satisfaction, but you lose a growth opportunity.")
        
        decision = input("Choose an option (1/2): ")
        if decision == '1':
            funds += 10_000_000
            for c in citizens_info:
                c["satisfaction"] = max(0, c["satisfaction"] - random.randint(5, 15))
            newspaper_headlines.append("Tech company arrives in the city! Concerns over pollution.")
            print("You accepted the offer. Funds increased! But citizens are less happy.")
        elif decision == '2':
            print("You rejected the offer. The city maintains its balance.")
            newspaper_headlines.append("Mayor rejects tech company offer; prioritizes wellbeing.")
        else:
            print("Invalid option. The mission is ignored.")
        update_citizen_satisfaction()
    input("\nPress Enter to continue...")

def elections():
    global mayor, days_to_elections
    clear_screen()
    print("!!! ELECTIONS !!!")
    print(f"Your approval rating is {citizen_satisfaction:.2f}%.")
    
    if citizen_satisfaction >= 70:
        print("Congratulations! You have been re-elected as mayor of Py.City for your excellent management.")
        newspaper_headlines.append(f"Mayor {mayor} re-elected with overwhelming citizen support!")
    elif citizen_satisfaction >= 40:
        print("You were re-elected, but it was close. Consider improving citizen satisfaction.")
        newspaper_headlines.append(f"Close re-election for Mayor {mayor}. Citizens demand change.")
    else:
        print("Unfortunately, your management did not please the people. You lost the election!")
        newspaper_headlines.append(f"Mayor {mayor} fails to win re-election! Their term has ended.")
        print(r"""
         ▄▄█▀▀▀▄█                                 ▄▄█▀▀██                            ▄█▄ 
        ▄█▀     ▀   ▄▄▄▄   ▄▄ ▄▄ ▄▄     ▄▄▄▄     ▄█▀     ██  ▄▄▄▄ ▄▄▄  ▄▄▄▄  ▄▄▄ ▄▄  ███ 
        ██    ▄▄▄▄ ▀▀ ▄██   ██ ██ ██  ▄█▄▄▄██    ██      ██  ▀█▄  █  ▄█▄▄▄██  ██▀ ▀▀ ▀█▀ 
        ▀█▄    ██  ▄█▀ ██   ██ ██ ██  ██         ▀█▄     ██   ▀█▄█   ██       ██      █  
         ▀▀█▄▄▄▀█  ▀█▄▄▀█▀ ▄██ ██ ██▄  ▀█▄▄▄▀     ▀▀█▄▄▄█▀     ▀█    ▀█▄▄▄▀  ▄██▄     ▄  
                                                                                     ▀█▀ 
        """)
        input("Press Enter to end the game...")
        exit()
    
    days_to_elections = elections_every_days  # Reset elections counter
    input("\nPress Enter to continue...")

def view_charts():
    clear_screen()
    print("📈 GROWTH CHARTS 📈")

    print("\nPopulation:")
    max_pop = max(population_history) if population_history else 1
    for i, pop in enumerate(population_history):
        bars = "█" * int((pop / max_pop) * 20)  # Scale to 20 characters
        print(f"Day {i+1}: {bars} {pop:,}")

    print("\nIncome vs Expenses (represented by Net Funds):")
    min_funds = min(funds_history) if funds_history else 0
    max_funds = max(funds_history) if funds_history else 1
    funds_range = max_funds - min_funds if max_funds != min_funds else 1

    for i, f in enumerate(funds_history):
        if funds_range > 0:
            bars = "█" * int(((f - min_funds) / funds_range) * 20)
        else:
            bars = "█" * 10 if f >= 0 else ""  # If only one value or zero range, show fixed bar
        print(f"Day {i+1}: {bars} ${f:,}")

    print("\nHappiness Level (Citizen Satisfaction):")
    for i, sat in enumerate(satisfaction_history):
        bars = "█" * int((sat / 100) * 20)  # Scale to 20 characters for 100%
        print(f"Day {i+1}: {bars} {sat:.2f}%")

    input("\nPress Enter to continue...")

def check_achievements():
    global achievements, citizens_count, funds, day

    # ACHIEVEMENTS - MONEY
    if "First 100 million in funds" not in achievements and funds >= 100_000_000:
        achievements.append("First 100 million in funds")
        print("\nACHIEVEMENT UNLOCKED: You reached $100,000,000 in funds!")
        newspaper_headlines.append("Py.City reaches one hundred million in funds!")
        input("Press Enter to continue...")

    if "Half a billion in funds" not in achievements and funds >= 500_000_000:
        achievements.append("Half a billion in funds")
        print("\nACHIEVEMENT UNLOCKED: You reached $500,000,000 in funds!")
        newspaper_headlines.append("Py.City reaches five hundred million in funds!")
        input("Press Enter to continue...")

    if "Billionaire Club" not in achievements and funds >= 1_000_000_000:
        achievements.append("Billionaire Club")
        print("\nACHIEVEMENT UNLOCKED: You reached $1,000,000,000!")
        newspaper_headlines.append("Py.City reaches a billion in funds!")
        input("Press Enter to continue...")
    
    # ACHIEVEMENTS - POPULATION
    if "First 2,000 citizens" not in achievements and citizens_count >= 2000:
        achievements.append("First 2,000 citizens")
        print("\nACHIEVEMENT UNLOCKED: You reached 2,000 citizens!")
        newspaper_headlines.append("Py.City's population surpasses 2,000 residents!")
        input("Press Enter to continue...")

    if "First 10,000 citizens" not in achievements and citizens_count >= 10000:
        achievements.append("First 10,000 citizens")
        print("\nACHIEVEMENT UNLOCKED: You reached 10,000 citizens!")
        newspaper_headlines.append("Py.City's population surpasses 10,000 residents!")
        input("Press Enter to continue...")

    # ACHIEVEMENTS - PROGRESS   
    if "Survivor of 30 days" not in achievements and day >= 30:
        achievements.append("Survivor of 30 days")
        print("\nACHIEVEMENT UNLOCKED: You survived 30 days without bankruptcy!")
        newspaper_headlines.append("The mayor shows resilience: 30 days of successful governance!")
        input("Press Enter to continue...")

def view_achievements():
    clear_screen()
    print("🎖️ YOUR ACHIEVEMENTS 🎖️")
    if not achievements:
        print("You haven't unlocked any achievements yet. Keep playing!")
    else:
        for a in achievements:
            print(f"- {a}")
    input("\nPress Enter to continue...")

def give_advice():
    clear_screen()
    print("🧠 TIPS FROM YOUR ADVISORS 🧠")
    
    # Economic Advisor
    if funds < 10_000_000:
        print(advisors["economic"])
    else:
        print("Economic Advisor: 'Your finances are stable for now. Good job!'")
    
    # Environmental Advisor
    if zone_wear["industrial"] > 70:
        print(advisors["environmental"])
    else:
        print("Environmental Advisor: 'The city's environment is holding up well.'")
    
    # Popularity Advisor
    if citizen_satisfaction < 60:
        print(advisors["popularity"])
    else:
        print("Popularity Advisor: 'Citizens are quite pleased with your management.'")
    
    input("\nPress Enter to continue...")

def build_special_zone():
    global funds, special_zones_built, newspaper_headlines
    clear_screen()
    print("\nSPECIAL ZONES AVAILABLE:")
    
    available_to_build = False
    for zone_name, info in special_zones_available.items():
        if not info["unlocked"]:
            requirement_met = True
            if "population_requirement" in info and len(citizens_info) < info["population_requirement"]:
                requirement_met = False
            
            if requirement_met:
                available_to_build = True
                print(f"{list(special_zones_available.keys()).index(zone_name) + 1}. {zone_name.capitalize()} (Cost: ${info['cost']:,})")
                if "population_requirement" in info:
                    print(f"   Requirement: {info['population_requirement']} citizens.")
            else:
                print(f"{list(special_zones_available.keys()).index(zone_name) + 1}. {zone_name.capitalize()} (Cost: ${info['cost']:,}) - REQUIRES {info.get('population_requirement', 'N/A')} citizens.")
        elif zone_name in special_zones_built:
            print(f"{zone_name.capitalize()} (ALREADY BUILT)")

    if not available_to_build:
        print("No new special zones are available to build yet or you already built all unlocked ones.")
        input("\nPress Enter to continue...")
        return

    choice_str = input("Select the special zone to build (number): ")
    try:
        choice_idx = int(choice_str) - 1
        chosen_zone_name = list(special_zones_available.keys())[choice_idx]
        chosen_zone_info = special_zones_available[chosen_zone_name]

        if chosen_zone_name in special_zones_built:
            print("This special zone has already been built.")
            input("\nPress Enter to continue...")
            return

        requirement_met = True
        if "population_requirement" in chosen_zone_info and len(citizens_info) < chosen_zone_info["population_requirement"]:
            requirement_met = False
            print(f"You do not meet the population requirement ({chosen_zone_info['population_requirement']} citizens).")

        if not requirement_met:
            input("\nPress Enter to continue...")
            return

        if funds >= chosen_zone_info["cost"]:
            funds -= chosen_zone_info["cost"]
            special_zones_built.append(chosen_zone_name)
            chosen_zone_info["unlocked"] = True  # Mark as unlocked (and built)
            print(f"{chosen_zone_name.capitalize()} built successfully!")
            newspaper_headlines.append(f"Grand opening of {chosen_zone_name.capitalize()} in Py.City!")

            # Apply special zone impacts
            if "satisfaction_impact" in chosen_zone_info:
                for c in citizens_info:
                    c["satisfaction"] = min(100, c["satisfaction"] + chosen_zone_info["satisfaction_impact"])
                update_citizen_satisfaction()
            if "funds_impact" in chosen_zone_info:
                funds += chosen_zone_info["funds_impact"]
            if "citizens_impact" in chosen_zone_info:
                global citizens_count
                for _ in range(chosen_zone_info["citizens_impact"]):
                    citizens_info.append(generate_citizen())
                citizens_count = len(citizens_info)
                update_citizen_satisfaction()

        else:
            print("You do not have enough funds to build this special zone.")
    except (ValueError, IndexError):
        print("Invalid option.")
    input("\nPress Enter to continue...")

# Finally, the actual interactive game loop.

def game_loop():
    while True:
        clear_screen()
        game_menu()
        option = input("Select an option: ")

        if option == '1':
            view_funds()
        elif option == '2':
            manage_policies()
        elif option == '3':
            build_zone_with_sectors()
        elif option == '4':
            manage_services()
        elif option == '5':
            view_city()
        elif option == '6':
            advance_day()
            if newspaper_headlines:
                show_daily_newspaper()
        elif option == '7':
            create_sector()
        elif option == '8':
            manage_public_transport()
        elif option == '9':
            view_charts()
        elif option == '10':
            view_achievements()
        elif option == '11':
            give_advice()
        elif option == '12':
            build_special_zone()
        elif option == '13':
            clear_screen()
            print("Thanks for playing Py.City.")
            break
        else:
            input("Invalid option. Press Enter to continue...")

# Run the main menu when executed directly.
if __name__ == "__main__":
    main_menu()

# Thank you for reading my annotations and giving the program a try.
# It took some late nights and a lot of inspiration to build — I don't know where it came from, but it happened.
# I used some libraries and constructs not covered in class (like os and time, and try/except blocks).
# Some choices may not be best practices, but they saved time while I experimented.
