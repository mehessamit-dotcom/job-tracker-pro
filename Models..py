# Import SQLite Module
import sqlite3
import numpy as np
from datetime import datetime





db = sqlite3.connect(r"C:\Users\hp\Documents\python\Jon tracker\job_tracker.db")
cr = db.cursor()

cr.execute(f"select * from applications ")
cat1 = cr.fetchall()

now = datetime.now()
now_date = now.strftime("%Y-%d-%m")

# Commit and close
def commit_close():
    # Save (commit) changes
    db.commit()
    # Close Database
    db.close()
    print("Connection to Database is closed")


class Functions:

    def __init__(self):
        # This method takes no arguments other than 'self'
        self.data = []

    def show_all_appl(self):

        cr.execute(f"select * from applications")
        all_appl = cr.fetchall()
        for i in range(1, len(all_appl)+1):

            cr.execute(f"select * from applications where id = {i}")
            results = cr.fetchall()

            if len(results) != 0:
                print(f"Applications number {i}:")
                for row in results:

                        print(f"Date of application : {row[1]},", end=" | ")

                        print(f"Role and Company => {row[3]} - {row[2]}/{row[4]}.", end=" | ")

                        print(f"Source => {row[5]}.", end=" | ")

                        print(f"Statut => {row[6]}.", end=" | ")

                        print(f"Tech Stack : {row[8]}", end=" | ")

                        print(f"Notes => {row[9]}.")

        commit_close()

    def show_specific_appl(self):

        for row in cat1: print(f"{row[0]}- {row[3]}/{row[2]} \n")
        uid = input("choose the application number or type a to add one")
        if uid == "a":

            return self.add_appl()
        else:
            cr.execute(f"select * from applications where id = '{uid}'")
            results = cr.fetchall()

            if len(results) == 0: print(f"You have no application with this id.")
            else:

                print(f"Application number {uid}:")
                for row in results:

                        print(f"Date of application : {row[1]},", end=" | ")

                        print(f"Role and Company => {row[3]} - {row[2]}/{row[4]}.", end=" | ")

                        print(f"Source => {row[5]}.", end=" | ")

                        print(f"Statut => {row[6]}.", end=" | ")

                        print(f"Salary => {row[7]}$.", end=" | ")

                        print(f"Tech Stack : {row[8]}", end=" | ")

                        print(f"Notes => {row[9]}.")


        commit_close()

    def add_statut(self):
        value = input("Write the statut :")
        while self.verify_statut(value) != True:
            print("Invalid statut. Valid options are: applied, interview, offer, rejected.")
            value = input("Write the statut :")
            return value

    def verify_statut(self, value):
        valid_status = ["applied", "interview", "offer", "rejected"]
        if value.lower() in valid_status:
            return True
        else: return False

    def change_statut(self, uid):
        c = input(f"Do you want to change the statut Y/N ?").strip().capitalize()

        if c == 'Y' or c == 'Yes' :
            statut = self.add_statut()
            cr.execute(f"update application set statut = '{statut}' where id = '{uid}'")

    def add_salary(self):
        value = input("Write the salary(Number) :")
        while self.verify_float(value) != True:
            print("Thats not a number")
            value = input("Write the salary(Number) :")
            return float(value)

    def verify_float(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def change_salary(self, uid):

        c = input(f"Do you want to change the stack Y/N ?").strip().capitalize()

        if c == 'Y' or c == 'Yes' :
            salary = self.add_salary()
            cr.execute(f"update application set salary = '{salary}' where id = '{uid}'")

    def add_stack(self):
        tech_list = []
        while True:
            tech = input("Add a technology to your stack (or type 'q' to quit): ").strip().capitalize()
            if tech.lower() == 'q':
                break
            tech_list.append(tech)
            tech_list = ', '.join(tech_list)
            return tech_list

    def change_stack(self, uid):

        c = input(f"Do you want to change the stack Y/N ?").strip().capitalize()

        if c == 'Y' or c == 'Yes' :
            stack = self.add_stack()
            cr.execute(f"update application set stack = '{stack}' where id = '{uid}'")

    def change_appl(self, uid, field):

        c = input(f"Do you want to change the {field} Y/N ?").strip().capitalize()

        if c == 'Y' or c == 'Yes' :
            statut = input(f"Write the new {field}:").strip().capitalize()
            cr.execute(f"update application set {field} = '{statut}' where id = '{uid}'")

    def add_from_role(self, comp, role):

        id = len(cat1)+2
        country = input("Write the country").strip().capitalize()
        source = input("Write the source").strip().capitalize()
        statut = self.add_statut()
        salary = self.add_salary()
        notes = input("Write the notes").strip().capitalize()
        tech_list = self.add_stack()

        cr.execute(
                f"insert into applications (id, date_applied, company, role, country, source, statut, salary, tech_stack, notes) values('{id}','{now_date}','{comp}','{role}','{country}','{source}','{statut}','{salary}','{tech_list}','{notes}')")

    def add_appl(self):

        role = input("Write the role :").strip().capitalize()
        comp = input("Write the company :").strip().capitalize()

        cr.execute(f"select * from applications where company = '{comp}' and role = '{role}'")
        results = cr.fetchone()

        if results == 1:

            print("You have this application already.")

            f = input("""You want to add a new one or add an interaction in the new one?
                      "a" => Add New depense
                      "s" => Add New interaction for the existing one
                      "q" => Quit the App
                      """)
            if f == 'a': self.add_from_role(comp, role)
            elif f == 's': self.add_new_interraction(results[0])
            else: pass

        elif results > 1:

            print("You have multiple applications for this role and company.")

            f = input("""You want to add a new one or add an interaction for an existing one?
                      "a" => Add New depense
                      "s" => Add New interaction for an existing one
                      "q" => Quit the App
                      """)

            if f == 'a': self.add_from_role(comp, role)

            elif f == 's':

                for row in results: print(f"Application id : {row[0]}, Date of application : {row[1]}")

                uid = input("Choose the application id you want to add an interction to :")
                self.add_new_interraction(uid)

        else: self.add_from_role(comp, role)

    def add_new_interraction(self, uid):

        interraction = input("Write description").strip().capitalize()
        notes = input("Write the notes").strip().capitalize()

        cr.execute(
                f"insert into interactions (application_id, date, interaction_type, notes) values('{uid}','{now_date}','{interraction}','{notes}')")

        self.change_statut(uid)

    def add_appl_inter(self):

        w = input("You want to add an application or an interaction : a/i").strip()

        if w == 'a' or w == 'application': self.add_appl()
        elif w == "i" or w == "interaction": self.add_new_interraction()
        else: print("Invalid command")

        commit_close()

    def update_appl(self):

        for row in cat1: print(f"{row[0]}- {row[3]}/{row[2]} \n")
        uid = input("choose the id of the application you want to update :")

        cr.execute(f"select * from applications where id = '{uid}'")
        results = cr.fetchall()

        if len(results) == 0: print(f"You have no application with this id.")
        else:
            print(f"Application number {uid}:")

            for row in results:

                    print(f"Date of application : {row[1]},", end=" | ")

                    print(f"Role and Company => {row[3]} - {row[2]}/{row[4]}.", end=" | ")
                    self.change_appl(row[0], 'role')
                    self.change_appl(row[0], 'company')
                    self.change_appl(row[0], 'country')
                    print(f"Source => {row[5]}.", end=" | ")
                    self.change_appl(row[0], 'source')
                    print(f"Statut => {row[6]}.", end=" | ")
                    self.change_statut(row[0])
                    print(f"Salary => {row[7]}$.", end=" | ")
                    self.change_salary(row[0])
                    print(f"Tech Stack : {row[8]}", end=" | ")
                    self.change_stack(row[0])
                    print(f"Notes => {row[9]}.")
                    self.change_appl(row[0], 'notes')

        commit_close()

    def update_appl_id(self, id):
        a= int(id)
        c = input(f"Do you want to update the ids after id = {id} Y/N ?").strip().capitalize()

        if c == 'Y' or c == 'Yes' :
            for row in cat1 :
                if int(row[0]) > int(id):
                    cr.execute(f"update applications set id = '{a}' where date_applied = '{row[1]}' and company = '{row[2]}' and role = '{row[3]}'")
                    a += 1

    def update_inter_id(self, id):
        a= int(id)
        c = input(f"Do you want to update the ids after id = {id} Y/N ?").strip().capitalize()

        if c == 'Y' or c == 'Yes' :
            cr.execute(f"select * from interactions")
            inter = cr.fetchall()
            for row in inter :
                if int(row[0]) > int(id):
                    cr.execute(f"update interactions set id = '{a}' where application_id = '{row[1]}' and date = '{row[2]}' and interaction_type = '{row[3]}'")
                    a += 1

    def delete_application(self):

        for row in cat1: print(f"{row[0]}- {row[3]}/{row[2]} \n")
        id = input("choose the id of the application you want to delete :")
        if int(id) > 0 and int(id) < len(cat1)+1:
            cr.execute(f"delete from applications where id = '{id}'")
            self.update_appl_id(id)
        else : print("Invalid command")

    def delete_interaction(self):

        uid = input("choose the id of the application you want to delete :")
        cr.execute(f"select * from interactions where application_id = '{uid}'")
        inter = cr.fetchall()
        for row in inter: print(f"{row[0]}- {row[3]}|{row[2]} : {row[4]} \n")
        id = input("choose the id of the interaction you want to delete :")

        if int(id) > 0 and int(id) < len(cat1)+1:
            cr.execute(f"delete from interactions where id = '{id}'")
            self.update_inter_id(id)
        else : print("Invalid command")

    def delete_appl_inter(self):

        w = input("You want to delete an application or an interaction : a/i").strip()

        if w == 'a' or w == 'application': self.delete_application()
        elif w == "i" or w == "interaction": self.delete_interaction()
        else: print("Invalid command")

        commit_close()

    def quit_app(self):

        print("quitting the app")

        commit_close()