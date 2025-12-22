import sqlite3
from datetime import datetime
import numpy as np
from Models import Functions as func

db = sqlite3.connect(r"C:\Users\hp\Documents\python\Jon tracker\job_tracker.db")

cr = db.cursor()

now = datetime.now()
now_date = now.strftime("%Y-%m-%d")
print(now_date)

fc = func()

# input big message
input_message = """
What do you want to do?
"s" => Show All Applications
"v" => Show a specific application
"a" => Add New application or an interaction
"d" => Delete an application or an interaction
"u" => Update an application
"q" => Quit the App
Choose Option:
"""
# Input message choose
user_input = input(input_message).strip().lower()

# Command list
commands_list = ["s", "a", "d", "u", "q","v"]

# check if Command is Exists
if user_input in commands_list:

    print(f"command {user_input} found")

else:

    print(f"Sorry this command \"{user_input}\" is not found")

if user_input=="s":

    fc.show_all_appl()

elif user_input=="v":

    fc.show_specific_appl()

elif user_input=="a":

    fc.add_appl_inter()

elif user_input=="d":

    fc.delete_appl_inter()

elif user_input=="u":

    fc.update_appl()

else:

    fc.quit_app()