# ---------- File Details --------------------------------------------------------------
# Name: initialise_database.py
# Version: 0.0.3
# Date Created:  14.07.2024 - 23:13
# Last Modified: 14.07.2024 - 23:52
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
    (1, 'English', 'An Inspector Calls', 'Single Response', 'Who is the author of "An Inspector Calls"?', 1, None, None, None, None, 'J.B. Priestley'),
    (2, 'English', 'An Inspector Calls', 'Single Response', 'In which year is the play "An Inspector Calls" set?', 1, None, None, None, None, '1912'),
    (3, 'English', 'An Inspector Calls', 'Single Response', 'Who is the mysterious inspector that arrives at the Birling household?', 1, None, None, None, None, 'Inspector Goole'),
    (4, 'English', 'An Inspector Calls', 'Single Response', 'Which character is the daughter of Arthur and Sybil Birling?', 1, None, None, None, None, 'Sheila Birling'),
    (5, 'English', 'An Inspector Calls', 'Multiple Choice', 'What is Arthur Birling\'s occupation?', 4, 'Doctor', 'Lawyer', 'Factory owner', 'Teacher', 'c'),
    (6, 'English', 'An Inspector Calls', 'Multiple Choice', 'Where does Gerald Croft tell Sheila he was during the summer?', 4, 'On a business trip', 'At the coast', 'Visiting his family', 'In London', 'd'),
    (7, 'English', 'An Inspector Calls', 'Multiple Choice', 'What is the inspector’s full name?', 4, 'Inspector Goole', 'Inspector Ghoul', 'Inspector Gould', 'Inspector Gale', 'a'),
    (8, 'English', 'An Inspector Calls', 'Multiple Choice', 'Which character is engaged to Sheila Birling?', 4, 'Eric Birling', 'Gerald Croft', 'Inspector Goole', 'Mr. Birling', 'b'),
    (9, 'English', 'An Inspector Calls', 'Multi-Response', 'Which of the following characters are part of the Birling family?', 4, 'Arthur', 'Eva', 'Sybil', 'Sheila', 'a,c,d'),
    (10, 'English', 'An Inspector Calls', 'Multi-Response', 'Which of these themes are explored in "An Inspector Calls"?', 4, 'Social responsibility', 'Capitalism', 'Gender inequality', 'Environmental issues', 'a,b,c'),
    (11, 'English', 'An Inspector Calls', 'Multi-Response', 'Which of the following actions were taken by members of the Birling family against Eva Smith?', 4, 'Firing her from a job', 'Denying her charity help', 'Evicting her from an apartment', 'Taking her to the hospital', 'a,b,c'),
    (12, 'English', 'An Inspector Calls', 'Multi-Response', 'Which of the following characters express remorse by the end of the play?', 4, 'Arthur Birling', 'Sheila Birling', 'Eric Birling', 'Gerald Croft', 'b,c'),
    (13, 'English', 'An Inspector Calls', 'True or False', '"An Inspector Calls" is set in 1912.', 1, None, None, None, None, 'True'),
    (14, 'English', 'An Inspector Calls', 'True or False', 'Eva Smith is revealed to be related to Inspector Goole.', 1, None, None, None, None, 'False'),
    (15, 'English', 'An Inspector Calls', 'True or False', 'Sheila Birling initially tries to deny any involvement in Eva Smith\'s life.', 1, None, None, None, None, 'True'),
    (16, 'English', 'An Inspector Calls', 'True or False', 'The play ends with the inspector revealing his true identity.', 1, None, None, None, None, 'False')
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
