# ---------- File Details --------------------------------------------------------------
# Name: initialise_database.py
# Version: 0.0.2
# Date Created:  14.07.2024 - 23:13
# Last Modified: 14.07.2024 - 23:46
# --------------------------------------------------------------------------------------


# [PREREQUISITES] - Modules and Configuration ------------------------------------------
import sqlite3  # Import the Module 'sqlite3'

# Establish Connection to SQLite Database File
conn = sqlite3.connect('database.db')
cursor = conn.cursor()  # Define Variable 'cursor'

# --------------------------------------------------------------------------------------


# Set-up Subjects Table ----------------------------------------------------------------

# Create 'subjects' table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER NOT NULL,
        name TEXT NOT NULL,
        PRIMARY KEY (name)
    )
''')

# Define the list of subjects with their details
subjects = [
    (1, 'English'),
    (2, 'Maths'),
    (3, 'Science')
]

# Insert data into the table
cursor.executemany('''
    INSERT INTO subjects
    (id, name)
    VALUES (?, ?)
''', subjects)

# --------------------------------------------------------------------------------------


# Set-up Topics Table ------------------------------------------------------------------

# Create 'topics' table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS topics (
        id INTEGER NOT NULL,
        subject TEXT NOT NULL,
        name TEXT NOT NULL,
        PRIMARY KEY (name),
        FOREIGN KEY (subject) REFERENCES subjects(name)
    )
''')

# Define the list of topics with their details
topics = [
    (1, 'English', 'An Inspector Calls'),
    (2, 'English', 'Poetry Anthology'),
    (3, 'English', 'Terminology'),
    (4, 'Maths', 'Key Formulas'),
    (5, 'Science', 'Biology'),
    (6, 'Science', 'Chemistry'),
    (7, 'Science', 'Physics')
]

# Insert data into the table
cursor.executemany('''
    INSERT INTO topics
    (id, subject, name)
    VALUES (?, ?, ?)
''', topics)

# --------------------------------------------------------------------------------------


# Set-up Questions Table ---------------------------------------------------------------

# Create 'questions' table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER NOT NULL,
        subject TEXT NOT NULL,
        topic TEXT NOT NULL,
        type TEXT NOT NULL,
        question TEXT NOT NULL,
        answers INTEGER,
        answer_a TEXT,
        answer_b TEXT,
        answer_c TEXT,
        answer_d TEXT,
        "correct_answer(s)" TEXT,
        FOREIGN KEY (subject) REFERENCES subjects(name),
        FOREIGN KEY (topic) REFERENCES topics(name)
    )
''')

# Define the list of questions with their details
questions = [
    
]

# Insert data into the table
cursor.executemany('''
    INSERT INTO questions
    (id, subject, topic, type, question, answers, answer_a, answer_b, answer_c, answer_d, "correct_answer(s)")
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', questions)

# --------------------------------------------------------------------------------------


# Commit Changes and Close Connection
conn.commit()
conn.close()

print("Database Initialised")  # Print Confirmation Message
