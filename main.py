# ---------- File Details ---------------------------------------------------------------------------------------------
# Name: main.py
# Version: 0.1.1
# Date Created:  15.07.2024 - 02:05
# Last Modified: 16.07.2024 - 01:25
# ---------------------------------------------------------------------------------------------------------------------


# [PREREQUISITES] - Modules and Configuration -------------------------------------------------------------------------

import sqlite3     # Import the Module 'sqlite3'
import random      # Import the Module 'random'

# Establish Connection to SQLite Database File
conn = sqlite3.connect('database.db')
cursor = conn.cursor()  # Define Variable 'cursor'

# ---------------------------------------------------------------------------------------------------------------------


# [SUBROUTINES] - The Program's Functions and Subprocesses ------------------------------------------------------------

# [SUBPROCESS] - Print a Dividing Line Terminal
def terminal_divide():
    print("\n-----------------------------------------------------------------------------------------\n")

# [SUBPROCESS] - List all Rows in a Given Query
def db_list_options(query):
    cursor.execute(query)
    rows = cursor.fetchall()
    num = 0
    for row in rows:
        num += 1
        print(f"{num}. {row[0]}")

# [SUBPROCESS] - Print a Welcome Message
def welcome_message():
    print("Welcome to The Think Tank!")
    input("\nAre you ready to enter?: ")

# [FUNCTION] - Return the User's Choice of Subject
def subject_select():
    print("Please Choose 1 of 3 Subjects")

    query = "SELECT name FROM subjects"
    db_list_options(query)

    choice = input("Select The Number of your Choice: ")

    cursor.execute(f"SELECT name FROM subjects WHERE id = {choice}")
    subject = cursor.fetchall()[0][0]

    return subject

# [FUNCTION] - Return the User's Choice of Topic
def topic_select(subject):
    print("Please Choose a Topic")

    query = f"SELECT name FROM topics WHERE subject = '{subject}'"
    db_list_options(query)

    choice = input("Select The Number of your Choice: ")

    cursor.execute(f"SELECT name FROM topics WHERE id = {choice}")
    topic = cursor.fetchall()[0][0]

    return topic

# [FUNCTION] - Load questions based on the user's choice
def load_questions(topic):
    print("Types of Questions")
    print("1. Single Response")
    print("2. Multiple Choice")
    print("3. Multi-Response")
    print("4. True or False")

    choice = input("Select Question Types (e.g. 1, 3, 4): ")
    choices = choice.split(", ")
    all_options = [
        "Single Response",
        "Multiple Choice",
        "Multi-Response",
        "True or False"
    ]
    selected_options = []

    for i in choices:
        selected_options.append(all_options[int(i) - 1])

    questions = []

    for option in selected_options:
        query = f"SELECT * FROM questions WHERE topic = '{topic}' AND type = '{option}'"
        cursor.execute(query)
        results = cursor.fetchall()
        questions.extend(results)

    return questions

# [SUBPROCESS] - Asks the Questions
def ask_questions(questions):
    random.shuffle(questions)

    count = 0
    score = 0
    mistakes = []

    print("\n-----------------------------------------------------------------------------------------\n")

    while True:
        for i in questions:
            count += 1

            if i[3] == "Single Response": # --------------------------------------------
                print(f"Question {count}:")
                print(f"{i[4]}")

                reply = input("Enter your answer: ")
                reply = reply.lower()

                if i[10] in reply:
                    score += 1
                    print(f"\nCorrect! Score: {score}/{count}\n")
                else:
                    print(f"\nIncorrect! Score: {score}/{count}\n")
                    mistakes.append([count, i[0], reply])
            # --------------------------------------------------------------------------

            if i[3] == "Multiple Choice": # --------------------------------------------
                print(f"Question {count}:")
                print(f"{i[4]}")

                characters = ["a", "b", "c", "d"]
                character_count = 0

                options = [i[6], i[7], i[8], i[9]]
                options = options[:i[5]]

                for option in options:
                    print(f"{characters[character_count]}. {option}")
                    character_count += 1

                reply = input("Enter your answer (e.g. a): ")
                reply = reply.lower()

                if i[10] in reply:
                    score += 1
                    print(f"\nCorrect! Score: {score}/{count}\n")
                else:
                    print(f"\nIncorrect! Score: {score}/{count}\n")
                    mistakes.append([count, i[0], reply])
            # --------------------------------------------------------------------------

            if i[3] == "Multi-Response": # --------------------------------------------
                print(f"Question {count}:")
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
                    score += 1
                    print(f"\nCorrect! Score: {score}/{count}\n")
                else:
                    print(f"\nIncorrect! Score: {score}/{count}\n")
                    mistakes.append([count, i[0], reply])
            # --------------------------------------------------------------------------

            if i[3] == "True or False": # --------------------------------------------
                    print(f"Question {count}:")
                    print(f"True or False: {i[4]}")

                    reply = input("Enter your answer: ")
                    reply = reply.lower()[0]

                    if i[10].lower()[0] in reply:
                        score += 1
                        print(f"\nCorrect! Score: {score}/{count}\n")
                    else:
                        print(f"\nIncorrect! Score: {score}/{count}\n")
                        mistakes.append([count, i[0], reply])
            # --------------------------------------------------------------------------

            if count % 5 == 0:
                check = input("Do you want to keep going? (y/n): ")
                print("")
                if check == "n":
                    break

        if len(mistakes) != 0: 
            mistake_view = input("Do you want to view your mistakes? (y/n): ")
            if mistake_view == "y":
                for i in mistakes:
                    query = f"SELECT correct_answer(s) FROM questions WHERE id = {i[2]}"
                    cursor.execute(query)
                    print(f"For Question {i[0]}, you entered {i[2]}, but the correct answer was {cursor.fetchall()}")

        print("\n-----------------------------------------------------------------------------------------\n")
        print(f"GAME OVER!! You Scored: {score}/{count}")
        play_again = input("Do you want to play again? (y/n): ")

        if play_again == "y":
            count = 0
        else:
            break

# ---------------------------------------------------------------------------------------------------------------------


# [MAIN PROGRAM] - The Program's Main Execution Flow ------------------------------------------------------------------

welcome_message()

terminal_divide()
subject = subject_select()

terminal_divide()
topic = topic_select(subject)

terminal_divide()
questions = load_questions(topic)

ask_questions(questions)

# ---------------------------------------------------------------------------------------------------------------------


# [POST-PROCESSING] - Close Connection to Database --------------------------------------------------------------------

conn.close()

# ---------------------------------------------------------------------------------------------------------------------
