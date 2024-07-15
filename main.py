# ---------- File Details --------------------------------------------------------------
# Name: main.py
# Version: 0.0.5
# Date Created:  15.07.2024 - 02:05
# Last Modified: 15.07.2024 - 02:14
# --------------------------------------------------------------------------------------

# [PREREQUISITES] - Modules and Configuration ------------------------------------------
import sqlite3  # Import the Module 'sqlite3'

# Establish Connection to SQLite Database File
conn = sqlite3.connect('database.db')
cursor = conn.cursor()  # Define Variable 'cursor'

# --------------------------------------------------------------------------------------


# [SUBROUTINES] - The Program's Functions and Subprocesses -----------------------------

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
    
    query = ("SELECT name FROM subjects")
    db_list_options(query)

    choice = input("Select The Number of your Choice: ")

    cursor.execute(f"SELECT name FROM subjects WHERE id = {choice}")
    subject = cursor.fetchall()[0][0]

    return subject

# [FUNCTION] - Return the User's Choice of Topic
def topic_select(subject):
    print("Please Choose a Topic")

    query = (f"SELECT name FROM topics WHERE subject = '{subject}'")
    db_list_options(query)

    choice = input("Select The Number of your Choice: ")

    cursor.execute(f"SELECT name FROM topics WHERE id = {choice}")
    topic = cursor.fetchall()[0][0]

    return topic

# --------------------------------------------------------------------------------------


# Main execution flow
print("\n-----------------------------------------------------------------------------------------\n")
welcome_message()
print("\n-----------------------------------------------------------------------------------------\n")
subject = subject_select()
print("\n-----------------------------------------------------------------------------------------\n")
topic = topic_select(subject)
print("\n-----------------------------------------------------------------------------------------\n")

