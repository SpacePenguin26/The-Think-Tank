# ---------- File Details ---------------------------------------------------------------------------------------------
# Name: main.py
# Version: 0.2.1
# Date Created:  15.07.2024 - 02:05
# Last Modified: 18.07.2024 - 00:09
# ---------------------------------------------------------------------------------------------------------------------


# [PREREQUISITES] - Modules and Configuration -------------------------------------------------------------------------

import sqlite3     # Import the Module 'sqlite3'
import random      # Import the Module 'random'
import pyfiglet    # Import the Module 'pyfiglet'

# Establish Connection to SQLite Database File
conn = sqlite3.connect('database.db')
cursor = conn.cursor()  # Define Variable 'cursor'

# Ascii Colour Codes
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

def answer_correct(score, count):
    score += 1
    print(f"\n{ascii_escape}{bc_green};{ts_bold}m Correct! {reset} Score: {score}/{count}")
    return score

def answer_incorrect(score, count, mistakes, i, reply):
    print(f"\n{ascii_escape}{bc_red};{ts_bold}m Incorrect! {reset} Score: {score}/{count}")
    mistakes.append([count, i[0], reply])
    return score

# [SUBPROCESS] - Print a Welcome Message
def welcome_message():
    print(pyfiglet.figlet_format("The Think Tank", font="slant"))
    print("Welcome to the Think Tank!")
    input("\n\nAre you ready to enter?: ")

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

                topic_options = sql_fetch(f"SELECT name FROM topics WHERE subject = '{subject}'")
                list_values(topic_options)

                choices = input("Select The Numbers of your Choices: ").replace(" ", "").split(",")

                for choice in choices:
                    topics.append(sql_fetch(f"SELECT name FROM topics WHERE id = {int(choice)}")[0][0])

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
def ask_questions(questions):
    random.shuffle(questions)

    count = 0
    score = 0
    mistakes = []

    terminal_divide_solid()

    while True:
        for i in questions:
            count += 1
            print("")
            
            print(f"{ascii_escape}{bc_cyan}m Question {count}: {reset}")

            try:
                if i[3] == "Single Response": # --------------------------------------------
                    print(f"{i[4]}")

                    reply = input("Enter your answer: ")
                    reply = reply.lower()

                    if i[10].lower() in reply:
                        score = answer_correct(score, count)
                    else:
                        score = answer_incorrect(score, count, mistakes, i, reply)
                # --------------------------------------------------------------------------

                if i[3] == "Multiple Choice": # --------------------------------------------
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

                if i[3] == "Multi-Response": # --------------------------------------------
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

                    print(f"Answer: {answer}, Reply: {reply}")

                    if answer == reply:
                        score = answer_correct(score, count)
                    else:
                        score = answer_incorrect(score, count, mistakes, i, reply)
                # --------------------------------------------------------------------------

                if i[3] == "True or False": # --------------------------------------------
                        print(f"True or False: {i[4]}")

                        reply = input("Enter your answer: ").lower()[0]

                        if i[10].lower()[0] in reply:
                            score = answer_correct(score, count)
                        else:
                            score = answer_incorrect(score, count, mistakes, i, reply)
                # --------------------------------------------------------------------------

                if count % 5 == 0:
                    check = input("Do you want to keep going? (y/n): ")
                    print("")
                    if check.lower() == "n":
                        break

            except (ValueError, IndexError) as e:
                print(f"Invalid input: {e}. Please try again.")

        terminal_divide_solid()
        print(f"GAME OVER!! You Scored: {score}/{count}")

        if len(mistakes) != 0: 
            mistake_view = input("Do you want to view your mistakes? (y/n): ")

            if mistake_view.lower() == "y":
                print("\nHere are your mistakes:")
                for i in mistakes:
                    mistake = sql_fetch(f'SELECT "correct_answer(s)" FROM questions WHERE id = {i[1]}')
                    print(f"Question {i[0]}: you entered '{i[2]}', but the correct answer was '{mistake[0][0]}'")

        play_again = input("Do you want to play again? (y/n): ")
        if play_again.lower() == "y":
            return True
        else:
            return False

# ---------------------------------------------------------------------------------------------------------------------


# [MAIN PROGRAM] - The Program's Main Execution Flow ------------------------------------------------------------------

def main():
    welcome_message()

    while True:
        terminal_divide_solid()
        subjects = subject_select()

        terminal_divide_dashed()
        topics = topic_select(subjects)

        terminal_divide_dashed()
        questions = load_questions(topics)

        play_again = ask_questions(questions)
        if not play_again:
            break

# Execute the main function
main()

# ---------------------------------------------------------------------------------------------------------------------


# [POST-PROCESSING] - Close Connection to Database --------------------------------------------------------------------

conn.close()

# ---------------------------------------------------------------------------------------------------------------------
