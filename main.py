# ---------- File Details ---------------------------------------------------------------------------------------------
# Name: main.py
# Version: 1.0.1
# Date Created:  15.07.2024 - 02:05
# Last Modified: 18.07.2024 - 02:48
# ---------------------------------------------------------------------------------------------------------------------

# [PREREQUISITES] - Modules and Configuration -------------------------------------------------------------------------

import sqlite3     # Import the Module 'sqlite3' for database operations
import random      # Import the Module 'random' for randomization tasks
import pyfiglet    # Import the Module 'pyfiglet' for ASCII art text
import getpass     # Import the Module 'getpass' for secure password input
import os          # Import the Module 'os' for system operations

# Establish Connection to SQLite Database File
conn = sqlite3.connect('database.db')  # Connect to SQLite database file 'database.db'
cursor = conn.cursor()  # Create a cursor object to execute SQL commands

# Ascii Colour Codes for terminal styling
ascii_escape = "\033["
reset = "\033[0m"

# Text Colour Codes
tc_black = "30"
tc_red = "31"
tc_green = "32"
tc_yellow = "33"
tc_blue = "34"
tc_magenta = "35"
tc_cyan = "36"
tc_white = "37"

# Text Style Codes
ts_none = "0"
ts_bold = "1"
ts_underline = "2"
ts_negative = "3"
ts_negative2 = "5"

# Background Colour Codes
bc_black = "40"
bc_red = "41"
bc_green = "42"
bc_yellow = "43"
bc_blue = "44"
bc_magenta = "45"
bc_cyan = "46"
bc_white = "47"

# ---------------------------------------------------------------------------------------------------------------------

# [SUBROUTINES] - The Program's Functions and Subprocesses ------------------------------------------------------------

# [SUBPROCESS] - Print a Dividing Line Terminal (Solid)
def terminal_divide_solid():
    print("\n-----------------------------------------------------------------------------------------")

# [SUBPROCESS] - Print a Dividing Line Terminal (Dashed)
def terminal_divide_dashed():
    print("\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")

# [FUNCTION] - Fetch Values from SQL Query Statement
def sql_fetch(query):
    cursor.execute(query)
    return cursor.fetchall()

# [FUNCTION] - Remove Duplicate Values from Given Array
def remove_duplicates(array):
    seen = set()
    result = []
    for value in array:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result

# [FUNCTION] - Extract First Elements from Given Array
def extract_first_elements(options):
    return [option[0] for option in options]

# [SUBPROCESS] - List all Values in a Given Query
def list_values(array):
    count = 0
    for value in array:
        count += 1
        # Adjust to handle tuples and print the first element
        if isinstance(value, tuple):
            print(f"{count}. {value[0]}")
        else:
            print(f"{count}. {value}")

# [FUNCTION] - Perform Actions of Correct Answer Given
def answer_correct(score, count):
    score += 1
    print(f"\n{ascii_escape}{bc_green};{ts_bold}m Correct! {reset} Score: {score}/{count}")
    return score

# [FUNCTION] - Perform Actions of Incorrect Answer Given
def answer_incorrect(score, count, mistakes, i, reply):
    print(f"\n{ascii_escape}{bc_red};{ts_bold}m Incorrect! {reset} Score: {score}/{count}")
    mistakes.append([count, i[0], reply])
    return score

# [FUNCTION] - Print a Welcome Message with Menu and Return Chosen Option
def welcome_message():
    os.system('cls||clear')  # Clear the screen for better user interface
    print(pyfiglet.figlet_format("The Think Tank", font="slant"))  # Print a stylized title
    print("Welcome to the Think Tank!\n")
    choice = main_menu()  # Display main menu options
    return choice

# [FUNCTION] - Print the Main Menu and Return Chosen Option
def main_menu():
    print(f"{ascii_escape}{ts_bold}mMain Menu{reset}")
    print("1. Enter the Think Tank")
    print("2. View the Leaderboard")
    print("3. Exit")

    while True:
        choice = input("Please select an option (1-3): ")
        if choice in ['1', '2', '3']:
            return choice
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

# [FUNCTION] - Create a New Account
def create_account():
    print("\nCreate a New Account")
    while True:
        username = input("Enter a username: ")
        password = getpass.getpass("Enter a password: ")
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            print("Account created successfully!")
            return username
        except sqlite3.IntegrityError:
            print("Username already taken. Please try again.")

# [FUNCTION] - Log In to an Existing Account
def log_in():
    print("\nLog In to Your Account")
    while True:
        username = input("Enter your username: ")
        password = getpass.getpass("Enter your password: ")

        # Check if the user is an admin (for demonstration, admin credentials are hardcoded)
        if username == "admin" and password == "adminpassword":
            print("Admin login successful!")
            return username, True  # Return True as second value to indicate admin
        else:
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            if cursor.fetchone():
                print("Login successful!")
                return username, False  # Return False as second value to indicate regular user
            else:
                print("Invalid username or password. Please try again.")

# [FUNCTION] - Return the User's Choice of Subjects
def subject_select():
    print(f"{ascii_escape}{tc_green}m                                    Subject Selection                                    {reset}")
    while True:
        try:
            print(f"\n{ascii_escape}{ts_bold}mChoose Your Subjects{reset}")

            subjects = sql_fetch("SELECT name FROM subjects")
            list_values(subjects)

            choices = input("Select The Numbers of your Choices (e.g. 1, 3): ").replace(" ", "").split(",")
            selected_subjects = []

            for choice in choices:
                cursor.execute(f"SELECT name FROM subjects WHERE id = {int(choice)}")
                subject = cursor.fetchall()[0][0]
                selected_subjects.append(subject)

            return selected_subjects

        except (ValueError, IndexError, sqlite3.Error) as e:
            print(f"Invalid input or database error: {e}. Please try again.")

# [FUNCTION] - Return the User's Choice of Topics
def topic_select(subjects):
    print(f"{ascii_escape}{tc_green}m                                     Topic Selection                                     {reset}")
    topics = []

    for subject in subjects:
        while True:
            try:
                print(f"\n{ascii_escape}{ts_bold}mChoose Topics for {subject}{reset}")

                # Fetch topics for the current subject
                topic_options = sql_fetch(f"SELECT name FROM topics WHERE subject = '{subject}'")
                list_values(topic_options)

                choices = input("Select The Numbers of your Choices: ").replace(" ", "").split(",")

                for choice in choices:
                    selected_topic = sql_fetch(f"SELECT name FROM topics WHERE id = {int(choice)}")
                    if selected_topic:
                        topics.append(selected_topic[0][0])

                break  # Break the while loop if no exception

            except (ValueError, IndexError, sqlite3.Error) as e:
                print(f"Invalid input or database error: {e}. Please try again.")

    return topics


# [FUNCTION] - Load questions based on the user's choices
def load_questions(topics):
    print(f"{ascii_escape}{tc_green}m                                 Question Type Selection                                 {reset}")

    fetched_options = []
    selected_options = []
    questions = []

    for topic in topics:
        fetched_options.extend(sql_fetch(f"SELECT type FROM questions WHERE topic = '{topic}'"))

    all_options = remove_duplicates(extract_first_elements(fetched_options))

    while True:
        try:
            print(f"\n{ascii_escape}{ts_bold}mChoose the Type of Questions{reset}")
            list_values(all_options)

            choice = input("Enter your Choice (e.g. 1, 3, 4): ")
            choices = choice.replace(" ", "").split(",")

            for i in choices:
                selected_options.append(all_options[int(i) - 1])

            for topic in topics:
                for option in selected_options:
                    questions.extend(sql_fetch(f"SELECT * FROM questions WHERE topic = '{topic}' AND type = '{option}'"))

            return questions

        except (ValueError, IndexError, sqlite3.Error) as e:
            print(f"Invalid input or database error: {e}. Please try again.")

# [SUBPROCESS] - Asks the Questions
def ask_questions(username, questions):
    random.shuffle(questions)

    count = 0
    score = 0
    mistakes = []
    asked_questions = set()  # Initialize a set to keep track of asked questions

    terminal_divide_solid()

    while True:
        for i in questions:
            if i[0] in asked_questions:  # Check if the question has already been asked
                continue  # Skip to the next question if this one has already been asked

            asked_questions.add(i[0])  # Add the question ID to the set of asked questions

            count += 1
            print("")

            print(f"{ascii_escape}{bc_cyan}m Question {count}: {reset}")

            try:
                if i[3] == "Single Response":  # --------------------------------------------
                    print(f"{i[4]}")

                    reply = input("Enter your answer: ")
                    reply = reply.lower()

                    if i[10].lower() in reply:
                        score = answer_correct(score, count)
                    else:
                        score = answer_incorrect(score, count, mistakes, i, reply)
                # --------------------------------------------------------------------------

                if i[3] == "Multiple Choice":  # --------------------------------------------
                    print(f"{i[4]}")

                    characters = ["a", "b", "c", "d"]
                    character_count = 0

                    options = [i[6], i[7], i[8], i[9]]
                    options = options[:i[5]]

                    for option in options:
                        print(f"{characters[character_count]}. {option}")
                        character_count += 1

                    reply = input("Enter your answer (e.g. a): ").lower()

                    if i[10].lower() in reply:
                        score = answer_correct(score, count)
                    else:
                        score = answer_incorrect(score, count, mistakes, i, reply)
                # --------------------------------------------------------------------------

                if i[3] == "Multi-Response":  # --------------------------------------------
                    print(f"{i[4]}")

                    characters = ["a", "b", "c", "d"]
                    character_count = 0

                    options = [i[6], i[7], i[8], i[9]]
                    options = options[:i[5]]

                    for option in options:
                        print(f"{characters[character_count]}. {option}")
                        character_count += 1

                    answer = i[10].replace(',', '').split()

                    reply = input("Enter your answer (e.g. a, c): ")
                    reply = sorted(reply.lower().replace(',', '').split())

                    if answer == reply:
                        score = answer_correct(score, count)
                    else:
                        score = answer_incorrect(score, count, mistakes, i, reply)
                # --------------------------------------------------------------------------

                if i[3] == "True or False":  # --------------------------------------------
                        print(f"True or False: {i[4]}")

                        reply = input("Enter your answer: ").lower()[0]

                        if i[10].lower()[0] in reply:
                            score = answer_correct(score, count)
                        else:
                            score = answer_incorrect(score, count, mistakes, i, reply)
                # --------------------------------------------------------------------------

                if count % 5 == 0:
                    check = input("\nDo you want to keep going? (y/n): ")
                    print("")
                    if check.lower() == "n":
                        break

            except (ValueError, IndexError) as e:
                print(f"Invalid input: {e}. Please try again.")

        terminal_divide_solid()
        print("")
        print(f"GAME OVER!! You Scored: {score}/{count}")

        save_scores(username, score, count)

        if len(mistakes) != 0:
            mistake_view = input("Do you want to view your mistakes? (y/n): ")

            if mistake_view.lower() == "y":
                print("\nHere are your mistakes:")
                for i in mistakes:
                    mistake = sql_fetch(f'SELECT "correct_answer(s)" FROM questions WHERE id = {i[1]}')
                    print(f"Question {i[0]}: you entered '{i[2]}', but the correct answer was '{mistake[0][0]}'")

        print("")
        play_again = input("Do you want to play again? (y/n): ")
        if play_again.lower() == "y":
            return True
        else:
            return False


# [SUBPROCESS] - View the Leaderboard
def view_leaderboard():
    terminal_divide_solid()
    print(f"{ascii_escape}{tc_green}m                                      Leaderboard                                      {reset}")
    print("")
    try:
        cursor.execute("SELECT username, score, questions_answered FROM leaderboard ORDER BY score DESC")
        leaderboard = cursor.fetchall()

        if not leaderboard:
            print("Leaderboard is empty.")
        else:
            count = 0
            for entry in leaderboard:
                count += 1
                print(f"{count}. Username: {entry[0]}, Score: {entry[1]}, Questions Answered: {entry[2]}")

    except sqlite3.Error as e:
        print(f"Error fetching leaderboard: {e}")
    print("")
    input("Press Enter to continue...")

# [FUNCTION] - Save Scores to Leaderboard (Updated to Handle Existing Records)
def save_scores(username, score, questions_answered):
    try:
        # Check if the user already exists in leaderboard
        cursor.execute("SELECT * FROM leaderboard WHERE username = ?", (username,))
        existing_entry = cursor.fetchone()

        if existing_entry:
            # Handle existing score and questions_answered properly
            current_score = int(existing_entry[2]) if isinstance(existing_entry[2], int) else 0
            current_questions_answered = int(existing_entry[3]) if isinstance(existing_entry[3], int) else 0

            updated_score = current_score + score
            updated_questions_answered = current_questions_answered + questions_answered

            cursor.execute("UPDATE leaderboard SET score = ?, questions_answered = ? WHERE username = ?",
                           (updated_score, updated_questions_answered, username))
        else:
            # Insert new record
            cursor.execute("INSERT INTO leaderboard (username, score, questions_answered) VALUES (?, ?, ?)",
                           (username, score, questions_answered))

        conn.commit()
        print("Scores saved successfully!")
    except sqlite3.Error as e:
        print(f"Error saving scores: {e}")

# ---------------------------------------------------------------------------------------------------------------------

# [MAIN PROGRAM] - The Program's Main Execution Flow ------------------------------------------------------------------
def main():
    username = None
    is_admin = False

    while True:
        if username is None:
            choice = welcome_message()  # Display welcome message and menu options

        if username is not None:
            choice = main_menu()  # Display main menu options

        if choice == '1':
            if username is None:
                print("\n1. Log In")
                print("2. Create an Account")
                auth_choice = input("Please select an option (1-2): ")

                if auth_choice == '1':
                    username, is_admin = log_in()  # Handle login process
                elif auth_choice == '2':
                    username = create_account()  # Handle account creation
                    is_admin = False
                else:
                    print("Invalid choice. Returning to main menu.")
                    continue

            terminal_divide_solid()
            subjects = subject_select()  # Select subjects for quiz

            if not subjects:  # Ensure subjects are fetched properly
                print("No subjects found. Please check your database.")
                continue

            terminal_divide_dashed()
            topics = topic_select(subjects)  # Select topics for quiz

            terminal_divide_dashed()
            questions = load_questions(topics)  # Load questions based on selected topics

            play_again = ask_questions(username, questions)  # Start the quiz
            if not play_again:
                username = None  # Reset username to None to indicate end of session
                is_admin = False  # Reset admin status
                os.system('cls||clear')

        elif choice == '2':
            view_leaderboard()  # View leaderboard

        elif choice == '3':
            print("Exiting the Think Tank. Goodbye!")  # Exit the program
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

# Execute the main function
main()

# ---------------------------------------------------------------------------------------------------------------------

# [POST-PROCESSING] - Close Connection to Database --------------------------------------------------------------------

conn.close()  # Close the SQLite database connection

# ---------------------------------------------------------------------------------------------------------------------
