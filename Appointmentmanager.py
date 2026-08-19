from datetime import datetime
from Appointment import Appointment
import json
import random as r

class AppointmentManager():
    def __init__(self):
        self.__appointment_list: list[Appointment] = []
        self.load_data()

    def add_appointment(self, user_id):
        max_id = 0
        for appointment in self.__appointment_list:
            try:
                if int(appointment.appointment_id) > max_id:
                    max_id = int(appointment.appointment_id)
            except (ValueError, TypeError):
                continue

        appointment_id = str(max_id + 1)

        while True:
            title = input("Enter appointment title: ").strip()
            if title:
                break
            print("Title cannot be empty.")

        while True:
            doctor = input("Enter doctor's name: ").strip()
            if doctor:
                break
            print("Doctor name cannot be empty.")

        while True:
            clinic = input("Enter clinic name: ").strip()
            if clinic:
                break
            print("Clinic name cannot be empty.")

        while True:
            date = input("Enter appointment date: ").strip()
            try:
                date = datetime.strptime(date, "%Y-%m-%d").date()
                if date < datetime.now().date():
                    print("Appointment date cannot be before today.")
                    continue
                break

            except ValueError:
                print("Invalid date, enter the date as %Y-%m-%d.")

        while True:
            time = input("Enter appointment time: ").strip()
            try:
                time = datetime.strptime(time, "%H:%M").time()

                appointment_datetime = datetime.combine(date, time)
                if appointment_datetime <= datetime.now():
                    print("Appointment must be in the future.")
                    continue
                break
            except ValueError:
                print("Invalid time, enter the time as %H:%M.")


        for appointment in self.__appointment_list:
            if str(appointment.user_id) == str(user_id) and appointment.date == date and appointment.time == time:
                print("You already have an appointment at this date and time exactly.")
                return

        # appointment_datetime = datetime.combine(date, time)
        # if appointment_datetime <= datetime.now():
        #     print("Appointment Must be in the future.")
        #     return

        notes = input("Enter notes (optional): ").strip()
        appointment = Appointment(appointment_id, user_id, title, doctor, clinic, date, time, notes)
        self.__appointment_list.append(appointment)
        self.save_data()

        print()
        print("Appointment added successfully.")
        messages = ["Don't forget your appointment!", "We wish you good health!", "Take care and arrive on time!", "Hope everything goes well!"]
        print(r.choice(messages))

    def view_appointments(self, user_id):
        user_appointments = []
        for appointment in self.__appointment_list:
            if str(appointment.user_id) == str(user_id):
                user_appointments.append(appointment)

        if len(user_appointments) == 0:
            print("There are no appointments to display.")
            return None

        print("=" * 40)
        for index, appointment in enumerate(user_appointments, start=1):
            print(f"{index}. {appointment}")
        print("=" * 40)
        return user_appointments

    def view_appointment_details(self, user_id):
        appointments = self.view_appointments(user_id)
        if appointments is None:
            return

        while True:
            try:
                choice = int(input("Enter appointment number to display its details: "))
                break
            except ValueError:
                print("Please enter a valid number.")

        if 1 <= choice <= len(appointments):
            appointment = appointments[choice - 1]
            print()
            print("========== Appointment Details ==========\n")
            appointment.display_info()
            print("-" * 35)
        else:
            print("Invalid appointment number.")

    def edit_appointment(self, user_id):
        appointments = self.view_appointments(user_id)
        if appointments is None:
            return

        while True:
            try:
                choice = int(input("Enter appointment number to edit: "))
                break
            except ValueError:
                print("Please enter a valid number.")

        if not 1 <= choice <= len(appointments):
            print("Invalid appointment number.")
            return

        appointment = appointments[choice - 1]

        print("1. Appointment title")
        print("2. Docter name")
        print("3. Clinic")
        print("4. Time")
        print("5. Date")
        print("6. Notes")
        print("7. Back")

        while True:
            try:
                edit_choice = int(input("Choose what you want to edit: "))
            except ValueError:
                print("Please enter a valid number.")
                continue

            if edit_choice == 1:
                while True:
                    new_title = input("Enter the new Title for the appoinment: ").strip()
                    if new_title:
                        break
                    print("Title cannot be empty.")
                appointment.title = new_title
                print("Title updated successfully.")

            elif edit_choice == 2:
                while True:
                    new_name = input("Enter new doctor name: ").strip()
                    if new_name:
                        break
                    print("Doctor name cannot be empty.")
                appointment.doctor = new_name
                print("Doctor updated successfully.")

            elif edit_choice == 3:
                while True:
                    new_clinic = input("Enter the New clinic of the appointment: ").strip()
                    if new_clinic:
                        break
                    print("Clinic cannot be empty.")
                appointment.clinic = new_clinic
                print("Clinic updated successfully.")

            elif edit_choice == 4:
                while True:
                    new_time = input("Enter time: ").strip()
                    try:
                        new_time = datetime.strptime(new_time, "%H:%M").time()
                    except ValueError:
                        print("Invalid time, enter the time as %H:%M.")
                        continue

                    new_datetime = datetime.combine(appointment.date, new_time)
                    if new_datetime <= datetime.now():
                        print("Appointment must be in the future.")
                        continue

                    conflict = False
                    for other_appointment in self.__appointment_list:
                        if other_appointment is appointment:
                            continue
                        if str(other_appointment.user_id) == str(user_id) and other_appointment.date == appointment.date and other_appointment.time == new_time:
                            conflict = True
                            break

                    if conflict:
                        print("You already have another appointment at this date and time.")
                        continue

                    break

                appointment.time = new_time
                print("Time of the Appointment updated successfully.")

            elif edit_choice == 5:
                while True:
                    new_date = input("Enter the new Date of the appointment: ").strip()
                    try:
                        new_date = datetime.strptime(new_date, "%Y-%m-%d").date()
                    except ValueError:
                        print("Invalid date, enter the date as %Y-%m-%d.")
                        continue

                    new_datetime = datetime.combine(new_date, appointment.time)
                    if new_datetime <= datetime.now():
                        print("Appointment must be in the future.")
                        continue

                    conflict = False
                    for other_appointment in self.__appointment_list:
                        if other_appointment is appointment:
                            continue
                        if str(other_appointment.user_id) == str(user_id) and other_appointment.date == new_date and other_appointment.time == appointment.time:
                            conflict = True
                            break

                    if conflict:
                        print("You already have another appointment at this date and time.")
                        continue

                    break

                appointment.date = new_date
                print("Date updated successfully.")

            elif edit_choice == 6:
                new_note = input("Enter the notes for this appointment: ").strip()
                appointment.notes = new_note
                print("Notes updated successfully.")

            elif edit_choice == 7:
                print("Edit cancelled.")
                return

            else:
                print("Invalid choice.")
                continue

            self.save_data()
            return

    def delete_appointment(self, user_id):
        appointments = self.view_appointments(user_id)
        if appointments is None:
            return

        while True:
            try:
                choice = int(input("\nEnter appointment number to delete: "))
                break
            except ValueError:
                print("Please enter a valid number.")

        if not 1 <= choice <= len(appointments):
            print("Invalid appointment number.")
            return

        appointment = appointments[choice - 1]
        ans = input(f"Are you sure you want to delete {appointment.title}? (y/n): ").strip().lower()

        if ans == "y":
            self.__appointment_list.remove(appointment)
            self.save_data()
            print("\nAppointment deleted successfully.")
        elif ans == "n":
            print("Removing appointment canceled")
        else:
            print("Invalid choice. Appointment was not deleted.")

    def search_appointment(self, user_id):
        user_appointments = []
        for appointment in self.__appointment_list:
            if str(appointment.user_id) == str(user_id):
                user_appointments.append(appointment)

        if len(user_appointments) == 0:
            print("There are no appointments to search.")
            return

        while True:
            search_title = input("Enter Appointment Title: ").strip().lower()
            flag = False

            for appoint in user_appointments:
                if search_title == str(appoint.title).lower():
                    print("======== Appointment Details ========\n")
                    appoint.display_info()
                    print()
                    input("Press Enter to continue...")
                    flag = True
                    break

            if flag:
                return

            print("\nThere is no Appointment with this title.")
            print("1. Search Again")
            print("2. Back")

            choice = input("Choose: ").strip()

            if choice == "1":
                continue
            elif choice == "2":
                return
            else:
                print("Invalid choice.")

    def update_appointment_status(self, user_id):
        appointments = self.view_appointments(user_id)
        if appointments is None:
            return

        while True:
            try:
                choice = int(input("Enter appointment number: "))
                break
            except ValueError:
                print("Please enter a valid number.")

        if not 1 <= choice <= len(appointments):
            print("Invalid appointment number.")
            return

        appointment = appointments[choice - 1]

        if appointment.status != "Upcoming":
            print(f"This appointment is already {appointment.status}.\n")
            ans = input("Do you want to change its status? (y/n): ").strip().lower()
            if ans != "y":
                return

        print("1. Mark as Completed")
        print("2. Mark as Missed")
        print("3. Cancel Appointment")
        print("4. Back")

        while True:
            try:
                option = int(input("Choose: "))
                break
            except ValueError:
                print("Please enter a valid number.")

        if option == 1:
            appointment.status = "Completed"
            print("Appointment marked as completed.")
        elif option == 2:
            appointment.status = "Missed"
            print("Appointment marked as missed.")
        elif option == 3:
            appointment.status = "Cancelled"
            print("Appointment cancelled.")
        elif option == 4:
            return
        else:
            print("Invalid choice.")
            return

        self.save_data()

    def save_data(self):
        data = []
        for appointment in self.__appointment_list:
            data.append(appointment.to_dict())

        with open("appointment.json", "w") as file:
            json.dump(data, file, indent=4)

    def load_data(self):
      try:
         with open("appointment.json", "r") as file:
            data = json.load(file)
      except FileNotFoundError:
        self.__appointment_list = []
        return

      self.__appointment_list = []
      for element in data:

         time=(datetime.strptime(element["time"], "%H:%M").time())
         date = datetime.strptime(element["date"],"%Y-%m-%d").date()
         appointment = Appointment(
            element["appointment_id"],
            element["user_id"],
            element["title"],
            element["doctor"],
            element["clinic"],
            date,
            time,       
            element["notes"],
            element.get("status", "Upcoming"))
         self.__appointment_list.append(appointment)


    def get_all_appointments(self, user_id):
        appointments = []

        for appointment in self.__appointment_list:
            if appointment.user_id == user_id:
                appointments.append(appointment)

        return appointments

    def get_all_appointments_for_notifications(self):
        return self.__appointment_list

    def view_today_appointments(self, user_id):
        today = datetime.now().date()
        found = False

        print()
        print("=" * 40)
        print("       TODAY'S APPOINTMENTS")
        print("=" * 40)

        for appointment in self.__appointment_list:
            if str(appointment.user_id) == str(user_id) and appointment.date == today:
                print(appointment)
                found = True
                print(f"Title  : {appointment.title}")
                print(f"Doctor : {appointment.doctor}")
                print(f"Clinic : {appointment.clinic}")
                print(f"Time   : {appointment.time}")
                print(f"Status : {appointment.status}")
                print("-" * 40)

        if not found:
            print("No appointments for today to display.")
