import os
# Dictionary to store game library with their quantities and rental costs
game_library = {
    "Donkey Kong": {"quantity": 3, "cost": 2},
    "Super Mario Bros": {"quantity": 5, "cost": 3},
    "Tetris": {"quantity": 2, "cost": 1},
}

# Dictionary to store user accounts with their balances and points
user_accounts = {}

# Admin account details
admin_username = "admin"
admin_password = "adminpass"

# Function to display available games with their numbers and rental costs
def display_available_games():
    print("\nGames Available: \n")
    for game, info in game_library.items():
        quantity = info["quantity"]
        cost = info["cost"]
        print(f"{game}: Quantity: {quantity}, Cost: ${cost}")


# Function to register a new user
def register_user():
    while True:
        print("\n\n**SIGN UP PAGE**\n")
        username = input("Enter a username: ")
        if not username:
            print("\nUsername cannot be empty.\n\n")
            continue
        elif username in user_accounts:
            print("Username already taken, please choose another username.")
            continue

        password = input("Enter a password: ")
        if not password:
            print("\nPassword cannot be empty.\n\n")
            continue

        initial_balance = float(input("Top-up is required. How much are you going to top up? $"))
        if initial_balance <= 0:
            print("Invalid top-up amount. Please enter a positive value.")
            continue

        user_accounts[username] = {"password": password, "balance": initial_balance, "points": 0, "inventory": []}
        print("Account registered successfully.\n")
        main()
        break


# Function to rent a game
def rent_game(username):
    display_available_games()  # Display available games first
    game_choice = input("Enter the name of the game you want to rent (or leave blank to cancel): ")
    if not game_choice:
        print("Transaction canceled.")
        return

    # Check if the chosen game is available
    if game_choice in game_library and game_library[game_choice]["quantity"] > 0:
        cost = game_library[game_choice]["cost"]
        user_balance = user_accounts[username]["balance"]

        if user_balance >= cost:
            # Deduct the cost from user's balance
            user_accounts[username]["balance"] -= cost
            # Add the game to the user's inventory
            user_accounts[username]["inventory"].append(game_choice)
            # Decrease the quantity of the game in the game library
            game_library[game_choice]["quantity"] -= 1
            # Update user's points based on the cost of the game
            user_accounts[username]["points"] += int(cost / 2)
            print(f"Game '{game_choice}' rented successfully!")
        else:
            print("Insufficient balance. Please top up your account.")

    else:
        print("Sorry, the game is either unavailable or does not exist in the library.")

    input("Press ENTER to continue.")

# Function to return a game
def return_game(username):
    display_inventory(username)  # Display user's inventory first
    game_to_return = input("Enter the name of the game you want to return (or leave blank to cancel): ")
    if not game_to_return:
        print("Transaction canceled.")
        return

    # Check if the game to return is in the user's inventory
    if game_to_return in user_accounts[username]["inventory"]:
        # Increase the quantity of the game in the game library
        game_library[game_to_return]["quantity"] += 1
        # Remove the game from the user's inventory
        user_accounts[username]["inventory"].remove(game_to_return)
        print(f"Game '{game_to_return}' returned successfully!")
    else:
        print("You don't have this game in your inventory.")

    input("Press ENTER to continue.")

# Function to top-up user account
def top_up_account(username, amount):
    user_accounts[username]["balance"] += amount
    print(f"Account topped up successfully. Current balance: ${user_accounts[username]['balance']}")
    input("Press ENTER to continue.")

# Function to display user's inventory
def display_inventory(username):
    print("\nYour Inventory:\n")
    inventory = user_accounts[username]["inventory"]
    if inventory:
        for game in inventory:
            print(game)
    else:
        print("Your inventory is empty.")

    input("\nPress ENTER to continue.")

def admin_update_game():
    display_available_games()
    game_to_update = input("Enter the name of the game you want to update (or leave blank to cancel): ")
    if not game_to_update:
        print("Update canceled.")
        return

    if game_to_update in game_library:
        new_quantity = int(input("Enter the new quantity: "))
        new_cost = float(input("Enter the new rental cost: $"))
        game_library[game_to_update]["quantity"] = new_quantity
        game_library[game_to_update]["cost"] = new_cost
        print("Game details updated successfully.")
    else:
        print("The game does not exist in the library.")

    input("Press ENTER to continue.")

# Function for admin login
def admin_login():
    while True:
        try:
            print("\n**ADMIN LOGIN PAGE**\n")
            admin = input("Username: ")
            if admin == admin_username:
                adminpass = input("Password: ")
                if adminpass == admin_password:
                    print("Login Successful")
                    admin_menu()
                else:
                    print("Invalid password")
            else:
                 print("Username is invalid")
                 
        except ValueError:
            print("Wrong input")
            input()
            return
        
# Admin menu
def admin_menu():
    while True:
        print("\n**ADMIN MENU**\n")
        print("1. Update Game Details")
        print("2. View Game Inventory")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")
        if choice == "1":
            admin_update_game()
        elif choice == "2":
            display_available_games()
        elif choice == "3":
            print("Exiting admin menu...")
            main()
            break
        else:
            print("Invalid input. Please try again.")


# Function for users to redeem points for a free game rental
def redeem_free_rental(username):
    points = user_accounts[username]["points"]
    if points >= 3:
        # Deduct 3 points and provide a free rental
        user_accounts[username]["points"] -= 3
        print("Congratulations! You've redeemed 3 points for a free game rental.")
        rent_game(username)  # Call the rent_game function to choose a free game
    else:
        print("Insufficient points to redeem for a free game rental.")
    input("\nPress ENTER to continue.")

# Function for the user's log in
def log_in():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    if username in user_accounts and user_accounts[username]["password"] == password:
        print("Log-in Success!!!.")
        logged_in_menu(username)
    else:
        print("Error. Invalid username or password.")

# Function for the user's logged in menu
def logged_in_menu(username):
    while True:
        print("\n**MENU**\n")
        print("1. View Games")
        print("2. My Inventory")
        print("3. Rent Game/s")
        print("4. Return Game/s")
        print("5. Top-up Account")
        print("6. Check Account Balance")
        print("7. Redeem points")
        print("8. Exit")

        choice = input("Enter your choice (1-8): ")
        if choice == "1":
            display_available_games()
        elif choice == "2":
            display_inventory(username)
        elif choice == "3":
            rent_game(username)
        elif choice == "4":
            return_game(username)
        elif choice == "5":
            amount = float(input("Enter the amount to top up: $"))
            top_up_account(username, amount)
        elif choice == "6":
            print(f"Your current balance is ${user_accounts[username]['balance']}")
            input("\nPress ENTER to continue.")
        elif choice == "7":
            redeem_free_rental(username)
        elif choice == "8":
            print("Exiting...")
            break
        else:
            print("Invalid input. Please try again.")

# Main function to run the program
def main():
    while True:
        try:
            print("\n**VIDEO GAME RENTAL**\n")
            print("1. View Available Games")
            print("2. Sign up/register")
            print("3. Log-in")
            print("4. Admin Log-in")
            print("5. Exit")

            choice = int(input("Enter your choice(1-5): "))
            if choice == 1:
                display_available_games()
                main()
            elif choice == 2:
                register_user()
            elif choice == 3:
                log_in()
            elif choice == 4:
                admin_login()
            elif choice == 5:
                print("Goodbye!")
                print("Exit")
                break
            else:
                print("Please enter a valid number.")

        except ValueError as e:
            print(e)

if __name__ == "__main__":
    main()


