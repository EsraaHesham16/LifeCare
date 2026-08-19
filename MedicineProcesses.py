import random as r
from datetime import datetime
from medicine import Medicine
import json


class MedicineProcesses:
    def __init__(self):
        
        self.__medicine_list: list[Medicine] = []
        self.load_data()

    def add_medicine(self, user_id):
        max_id = 0
        for medicine in self.__medicine_list:
            if int(medicine.medicine_id) > max_id:
                max_id = int(medicine.medicine_id)
        medicine_id = max_id + 1

        while True:
            name = input("Enter The Medicine Name: ").strip()
            if name:
                break
            print("Medicine name cannot be empty.")

        for medicine in self.__medicine_list:
            if medicine.user_id == user_id and medicine.medicine_name.lower() == name.lower():
                print("This medicine already exists.")
                return

        dose = input("Enter The prescribed dose: ").strip()
        while True:
            try:
                times_per_day = int(input("How many doses per day? "))
                if times_per_day <= 0:
                    print("Number of doses must be greater than 0.")
                    continue
                break
            except ValueError:
                print("Please enter a valid number.")

        times = []
        for i in range(times_per_day):
            while True:
                t = input(f"Enter time {i + 1} (HH:MM): ").strip()
                try:
                    t = datetime.strptime(t, "%H:%M").time()
                    if t in times:
                        print("Times cannot be duplicated.")
                        continue
                    times.append(t)
                    break
                except ValueError:
                    print("Invalid time. Enter the time as HH:MM.")

        while True:
            start_date = input("Enter the start date for This Medicine (YYYY-MM-DD): ").strip()
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()

                if start_date < datetime.now().date():
                    print("Start date MUST be today date or after that not before!")
                    continue
                break
            except ValueError:
                print("Invalid date. Enter the date as YYYY-MM-DD.")

        while True:
            end_date = input("Enter the end date for This Medicine (YYYY-MM-DD): ").strip()
            try:
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                if end_date < start_date:
                    print("End date cannot be before start date.")
                    continue
                break
            except ValueError:
                print("Invalid date. Enter the date as YYYY-MM-DD.")

        medicine = Medicine(medicine_id, user_id, name, dose, times_per_day, times, start_date, end_date)
        self.__medicine_list.append(medicine)
        self.save_data()

        print()
        support_sentences = [
            "I hope you're on the road to recovery",
            "Take care and get plenty of rest",
            "Hope you recover quickly",
            "Wishing you all the best with your treatment",
            "Stay strong—you've got this! Wishing you a speedy recovery",
            "Get well soon",
            "Wishing you a speedy recovery",
            "Hope you feel better soon"
        ]
        print("The Medicine Has been Added to your Medicines successfully")
        print(r.choice(support_sentences))
        return medicine

    def view_medicines(self, user_id):
        user_medicines = []
        for medicine in self.__medicine_list:
            if medicine.user_id == user_id:
                user_medicines.append(medicine)

        if len(user_medicines) == 0:
            print("There are no medicines to display.")
            return None

        medicines = user_medicines

        print("=" * 40)
        for index, medicine in enumerate(medicines, start=1):
            print(f"{index}. {medicine}")
        return medicines

    def view_medicine_details(self, user_id):
        medicines = self.view_medicines(user_id)
        if medicines is None:
            return

        try:
            choice = int(input("Enter medicine number: "))
        except ValueError:
            print("Invalid choice.")
            return

        if 1 <= choice <= len(medicines):
            medicine = medicines[choice - 1]
            print()
            print("========== Medicine Details ==========\n")
            medicine.display_info()
            print("-" * 35)
        else:
            print("Invalid choice.")

    def edit_medicine(self, user_id):
        medicines = self.view_medicines(user_id)
        if medicines is None:
            return

        try:
            choice = int(input("Enter medicine number: "))
        except ValueError:
            print("Invalid choice.")
            return

        if not (1 <= choice <= len(medicines)):
            print("Invalid medicine number.")
            return

        medicine = medicines[choice - 1]
        print(f"What do you want to edit about {medicine}?")
        print()
        print("1. Medicine Name")
        print("2. Dose")
        print("3. Times Per Day")
        print("4. Times")
        print("5. Start Date")
        print("6. End Date")
        print("7. Back")

        while True:
            try:
                edit_choice = int(input("Choose what you want to edit: "))
            except ValueError:
                print("Please enter a valid number.")
                continue

            if edit_choice == 1:
                while True:
                    new_name = input("Enter the new name of the medicine: ").strip()
                    if not new_name:
                        print("Medicine name cannot be empty.")
                        continue
                    duplicate = False
                    for other_medicine in self.__medicine_list:
                        if other_medicine is not medicine and other_medicine.user_id == user_id and other_medicine.medicine_name.lower() == new_name.lower():
                            duplicate = True
                            break
                    if duplicate:
                        print("This medicine already exists.")
                        continue
                    break
                medicine.medicine_name = new_name
                print("Medicine Name updated successfully")

            elif edit_choice == 2:
                new_dose = input("Enter new dose: ").strip()
                if not new_dose:
                    print("Dose cannot be empty.")
                    continue
                medicine.dose = new_dose
                print("Medicine doses updated successfully")

            elif edit_choice == 3:
                while True:
                    try:
                        new_times_per_day = int(input("Enter the New number of times per day: "))
                        if new_times_per_day <= 0:
                            print("Number of doses must be greater than 0.")
                            continue
                        break
                    except ValueError:
                        print("Please enter a valid number.")

                new_times = []
                for i in range(new_times_per_day):
                    while True:
                        t = input(f"Enter time {i + 1} (HH:MM): ").strip()
                        try:
                            t = datetime.strptime(t, "%H:%M").time()
                            if t in new_times:
                                print("Times cannot be duplicated.")
                                continue
                            new_times.append(t)
                            break
                        except ValueError:
                            print("Invalid time. Enter the time as HH:MM.")

                medicine.times_per_day = new_times_per_day
                medicine.times = new_times
                print("Medicine updated successfully")

            elif edit_choice == 4:
                print(f"Remember you've entered that medicine must be taken for {medicine.times_per_day} times")
                new_times = []
                for i in range(medicine.times_per_day):
                    while True:
                        t = input(f"Enter time {i + 1} (HH:MM): ").strip()
                        try:
                            t = datetime.strptime(t, "%H:%M").time()
                            if t in new_times:
                                print("Times cannot be duplicated.")
                                continue
                            new_times.append(t)
                            break
                        except ValueError:
                            print("Invalid time. Enter the time as HH:MM.")
                medicine.times = new_times
                print("Medicine updated successfully")

            elif edit_choice == 5:
                while True:
                    new_start = input("Enter the new Start Date (YYYY-MM-DD): ").strip()
                    try:
                        new_start = datetime.strptime(new_start, "%Y-%m-%d").date()
                        if new_start > medicine.end_date:
                            print("Start date cannot be after end date.")
                            continue
                        break
                    except ValueError:
                        print("Invalid date. Enter the date as YYYY-MM-DD.")
                medicine.start_date = new_start
                print("Medicine updated successfully")

            elif edit_choice == 6:
                while True:
                    new_end = input("Enter the new End Date (YYYY-MM-DD): ").strip()
                    try:
                        new_end = datetime.strptime(new_end, "%Y-%m-%d").date()
                        if new_end < medicine.start_date:
                            print("End date cannot be before start date.")
                            continue
                        break
                    except ValueError:
                        print("Invalid date. Enter the date as YYYY-MM-DD.")
                medicine.end_date = new_end
                print("Medicine updated successfully")

            elif edit_choice == 7:
                print("Edit cancelled.")
                return

            else:
                print("Invalid choice.")
                continue

            self.save_data()

    def delete_medicine(self, user_id):
        medicines = self.view_medicines(user_id)
        if medicines is None:
            return

        try:
            choice = int(input("Enter medicine number: "))
        except ValueError:
            print("Invalid choice.")
            return

        if not (1 <= choice <= len(medicines)):
            print("Invalid medicine number.")
            return

        medicine = medicines[choice - 1]
        ans = input(f"Are you sure you want to remove {medicine}? (y/n): ").strip().lower()

        if ans == "y" or ans == "yes":
            self.__medicine_list.remove(medicine)
            self.save_data()
            print(f"Removing {medicine} done successfully")
        elif ans == "n" or ans == "no":
            print(f"Removing {medicine} canceled")
        else:
            print("Invalid input")

    def search_medicine(self, user_id):
        user_medicines = []
        for medicine in self.__medicine_list:
            if medicine.user_id == user_id:
                user_medicines.append(medicine)

        if not user_medicines:
            print("There are no medicines.")
            return

        while True:
            search_name = input("Enter medicine name: ").strip().lower()
            if not search_name:
                print("Medicine name cannot be empty.")
                continue

            matching_medicines = []
            for medicine in user_medicines:
                if search_name in medicine.medicine_name.lower():
                    matching_medicines.append(medicine)

            if len(matching_medicines) == 0:
                print("\nThere is no Medicine with this name.")
                print("1. Search Again")
                print("2. Back")
                user_choice = input("Choose: ").strip()

                if user_choice == "1":
                    continue
                elif user_choice == "2":
                    return
                else:
                    print("Invalid choice.")
                    continue

            print()
            print("Matching Medicines:\n")
            for index, medicine in enumerate(matching_medicines, start=1):
                print(f"{index}. {medicine}")
            print("0. Back")

            try:
                choice = int(input("\nChoose medicine number: "))
            except ValueError:
                print("Invalid choice.")
                continue

            if choice == 0:
                return
            elif 1 <= choice <= len(matching_medicines):
                selected = matching_medicines[choice - 1]
                print()
                print("========== Medicine Details ==========\n")
                selected.display_info()
                print()
                input("Press Enter to continue...")
            else:
                print("Invalid choice.")

    def mark_dose_taken(self, user_id):
        medicines = self.view_medicines(user_id)
        if medicines is None:
            print("There are no medicines to show doses.")
            return

        try:
            choice = int(input("Enter medicine number: "))
        except ValueError:
            print("Invalid choice.")
            return

        if not (1 <= choice <= len(medicines)):
            print("Invalid medicine number.")
            return

        medicine = medicines[choice - 1]
        today = datetime.now().strftime("%Y-%m-%d")

        if today not in medicine.taken:
            medicine.taken[today] = [False] * medicine.times_per_day

        print()
        print("Today's Doses:")

        for i in range(medicine.times_per_day):
            if medicine.taken[today][i]:
                status = "Taken"
            else:
                status = "Not Taken"
            print(f"{i + 1}. {medicine.times[i]} - {status}")

        try:
            dose = int(input("Choose dose number to mark as TAKEN: "))
        except ValueError:
            print("Invalid dose number.")
            return

        if 1 <= dose <= medicine.times_per_day:
            if medicine.taken[today][dose - 1]:
                print("This dose has already been marked as taken today.")
                return
            medicine.taken[today][dose - 1] = True
            print("Dose marked as taken successfully.")
            print("Wish you a speedy recovery :D")
            self.save_data()
        else:
            print("Invalid dose number.")

    def save_data(self):
        data = []
        for medicine in self.__medicine_list:
            data.append(medicine.to_dict())

        with open("medicine.json", "w") as file:
            json.dump(data, file, indent=4)

    def load_data(self):
        try:
            with open("medicine.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            self.__medicine_list = []
            return

        self.__medicine_list = []

        for item in data:
            times = []
            for t in item["times"]:
                times.append(datetime.strptime(t, "%H:%M").time())

            start_date = datetime.strptime(item["start_date"], "%Y-%m-%d").date()
            end_date = datetime.strptime(item["end_date"], "%Y-%m-%d").date()
            taken = item.get("taken", {})

            medicine = Medicine(
                item["medicine_id"],
                item["user_id"],
                item["medicine_name"],
                item["dose"],
                item["times_per_day"],
                times,
                start_date,
                end_date,
                taken=taken,
                completion_notified=item.get("completion_notified", False),
                reminder_notified=item.get("reminder_notified", False)
            )
            self.__medicine_list.append(medicine)

    def get_all_medicines(self, user_id):
        medicines = []
        for medicine in self.__medicine_list:
            if medicine.user_id == user_id:
                medicines.append(medicine)
        return medicines
    def get_all_medicines_for_notifications(self):
        return self.__medicine_list

    def show_notifications(self, user_id):
        today = datetime.now().date()
        notifications = []
        medicines_to_remove = []

        for medicine in self.__medicine_list:
            if medicine.user_id != user_id:
                continue

            if today > medicine.end_date and not medicine.completion_notified:
                notifications.append(f"You have completed {medicine.medicine_name}.")
                notifications.append(
                    "We hope you're feeling much better.\nDon't forget to consult your doctor if symptoms continue.")
                medicine.completion_notified = True

                choice = input("Do you want to remove this medicine? (y/n): ").strip().lower()

                if choice == "y" or choice == "yes":
                    medicines_to_remove.append(medicine)
                    print("Medicine removed successfully.")

                self.save_data()

            elif (medicine.end_date - today).days == 1 and not medicine.reminder_notified:
                notifications.append(f"{medicine.medicine_name} will finish tomorrow.")
                medicine.reminder_notified = True
                self.save_data()

            elif today == medicine.end_date:
                notifications.append(f"Today is the last day for {medicine.medicine_name}.")

        for medicine in medicines_to_remove:
            self.__medicine_list.remove(medicine)

        self.save_data()

        print("=" * 40)
        print("        Notifications        ")
        print("=" * 40)

        if len(notifications) == 0:
            print("No new notifications today.")
        else:
            for noti in notifications:
                print(noti)
                print()
                print("-" * 40)

        print("Stay healthy and have a nice day!")
        input("Press Enter to continue...")
        print("=" * 40)

