from User import User
from water import WaterTracker
from sleep import SleepTracker
from activity_tracker import ActivityTracker
from mood_tracker import MoodTracker
from dashboard import DashBoard
from report  import Reports
from MedicineProcesses import MedicineProcesses
from Appointmentmanager import AppointmentManager
from calories import Calories
from goals import Goals
from todo import To_Do
medicine_manager=MedicineProcesses()
appointment_manager=AppointmentManager()
user1=User()
program=False


def open_program():
    global program
    global user_id
    print(f"{"="*20}WELCOME TO LIFE CARE{"="*20}\n")
    print("Let's get started!\n")
    
    while True:
        print(f"1.Register\n2.Login\n3.Exit")
        choice = input("Enter your choice:")
        if choice=="1" or choice=="register":
            print("\nPlease enter your information")
            user_id = user1.register()
            if user_id:
                program = True
                break
        elif choice=="2" or choice=="login":           
            user_id=user1.login()
            if user_id:
                program = True
                break
        elif choice=="3" or choice=="exit":
            print("Goodbye!")
            break
        else:
            print("Invalid")
def profile():
    global program
    while True:
        print(f"\n1.Show Profile\n2.Edit Profile\n3.Delete Account\n4.Logout\n5.Back")
        user_choice = input("Enter your choice:")
        if user_choice == "1" or user_choice == "show Profile":
            user1.show_profile()
            input(f"\nPress Enter to continue..")
            continue
        elif user_choice == "2" or user_choice == "edit Profile":
            user1.edit_profile()
            input(f"\nPress Enter to continue..")
            continue
        elif user_choice == "3" or user_choice == "delete Account":
            user1.delete_account()
            input(f"\n Press Enter to continue..")
            program=False
            break
        elif user_choice == "4" or user_choice == "logout":
            program=False
            open_program()     
            break
        elif user_choice=="5":
            return
        else:
            print("Invalid")
def water():
    person = WaterTracker(user_id)
    print("========= Water Tracker ===========")
    print("Today's Goal: 8")
    while True:
        option = int(input("1.Add cup\n2.View today's water\n3.View history water\n4.back"))
        if option == 1:
            person.add_cup()
        elif option == 2:
            person.view_today_water()
        elif option == 3:
            person.view_history()
        elif option == 4:
            break
        else:
            print("invalid option\nPlease enter(1,2,3): ")
        input("press enter to continue")
def sleep():
    person = SleepTracker(user_id)
    print("========= Sleep Tracker =============")
    while True:
        option = int(input("1.Add Today's Sleep\n2.View Today's Sleep\n3.View Sleep History\n4.back"))
        if option == 1:
            person.add_sleep()
        elif option == 2:
            person.view_today_sleep()
        elif option == 3:
            person.view_Sleep_history()
        elif option == 4:
            break
        else:
            print("invalid option. Please enter(1, 2, 3, 4): ")
        input("press enter to continue.")
def medicines_menu(medicine_manager, user_id):
    medicine_manager.show_notifications(user_id)
    input("\nPress Enter to continue...")
    while True:
        print("=" * 40)
        print("         MEDICINES MENU")
        print("=" * 40)
        print("1. Add Medicine")
        print("2. View All Medicines")
        print("3. View Medicine Details")
        print("4. Search Medicine")
        print("5. Edit Medicine")
        print("6. Delete Medicine")
        print("7. Mark Dose as Taken")
        print("8. Back")
        print("=" * 40)

        choice = input("Choose an option: ")

        if choice == "1":
            medicine_manager.add_medicine(user_id)

        elif choice == "2":
            medicine_manager.view_medicines(user_id)

        elif choice == "3":
            medicine_manager.view_medicine_details(user_id)

        elif choice == "4":
            medicine_manager.search_medicine(user_id)

        elif choice == "5":
            medicine_manager.edit_medicine(user_id)

        elif choice == "6":
            medicine_manager.delete_medicine(user_id)

        elif choice == "7":
            medicine_manager.mark_dose_taken(user_id)
        elif choice == "8":
            break

        else:
            print("Invalid choice. Please try again.")

def appointments_menu(appointment_manager, user_id):
    while True:
        print("=" * 40)
        print("         APPOINTMENTS MENU")
        print("=" * 40)
        print("1. Add Appointment")
        print("2. View All Appointments")
        print("3. View Appointment Details")
        print("4. Search Appointment")
        print("5. Edit Appointment")
        print("6. Delete Appointment")
        print("7. Update Appointment Status")
        print("8. View Today's Appointments")
        print("9. Back")
        print("=" * 40)

        choice = input("Choose an option: ")

        if choice == "1":
            appointment_manager.add_appointment(user_id)

        elif choice == "2":
            appointment_manager.view_appointments(user_id)

        elif choice == "3":
            appointment_manager.view_appointment_details(user_id)

        elif choice == "4":
            appointment_manager.search_appointment(user_id)

        elif choice == "5":
            appointment_manager.edit_appointment(user_id)

        elif choice == "6":
            appointment_manager.delete_appointment(user_id)

        elif choice == "7":
            appointment_manager.update_status(user_id)

        elif choice == "8":
            appointment_manager.view_today_appointments(user_id)

        elif choice == "9":
            break

        else:
            print("Invalid choice. Please try again.")
def mood():
    while True:
        mood=MoodTracker(user_id)
        print("1.add mood\n2.view today mood\n3.delete mood by date\n4.edit mood by date\n5.streak of mood\n6.get mood by date\n7.back")
        mood_choice = input("choose number: ")
        if mood_choice == "1":
            mood.add_mood()
        elif mood_choice == "2":
            mood.view_today_mood()
        elif mood_choice == "3":
            mood.delete_mood()
        elif mood_choice == "4":
            mood.edit_mood()
        elif mood_choice == "5":
            mood.streak()
        elif mood_choice == "6":
            mood.get_by_date()
        elif mood_choice == "7":
            break
        else:
            print("invalid input!\ntry again.")
def activity():
    while True:
        activity=ActivityTracker(user_id)
        print("1.add activity\n2.view today activity\n3.delete activity by date\n4.edit activity by date\n5.streak of activity\n6.get activity by date\n7.back")
        activity_choice=input("choose number: ")
        if activity_choice=="1":
            activity.add_activity()
        elif activity_choice=="2":
            activity.view_today_activity()
        elif activity_choice=="3":
            activity.delete_activity()
        elif activity_choice=="4":
            activity.edit_activity()
        elif activity_choice=="5":
            activity.streak()
        elif activity_choice=="6":
            activity.get_by_date()
        elif activity_choice=="7":
            break
        else:
            print("invalid input!\ntry again.")
def report(user_id):
    report= Reports()
    print("1- daily report")
    print("2- weekly report")
    print("3- monthly report")

    choice = input("choose: ")
    if choice == "1":
        report.daily_report(user_id)
    elif choice == "2":
        report.weekly_report(user_id)
    elif choice == "3":
        report.monthly_report(user_id)
    else:
        print("invalid choice")

def goals():
    goal=Goals()
    goal.menu(user_id)

def calories():
    while True:
    person = Calories(user_id)
    print(f'{"="*10} {"calories list"} {"="*10}')
    option=input("1.add your data\n2.get your BMI\n3.get your TDEE (calories you need)\n4.add calories you have today\n5.show your progress in your daily need of calories\n6.edit on your data\n7.show your data\n8.suggestions to your meals\n9.back\n")
    if option == "1":
        person.add_data()
    elif option =="2":
        person.calculate_bmi()
    elif option == "3":
        person.calculate_calories()
    elif option == "4":
        person.add_calorie()
    elif option == "5":
        person.progress()
    elif option == "6":
        person.edit_data()
    elif option == "7":
        person.get_data()
    elif option == "8":
        person.suggestions()
    elif option == "9":
        break
    else:
        print("invalid input!\nplease try again")
    enter=input("press to continue...")
def to_do():
    while True:
        print(f"{"=" * 10} TO-DO LIST {"=" * 10}")
        user = To_Do(user_id)
        print(f"1.Add Task/n2.View Task\n3.Edit Task\n4.Delete Task\n5.Mark task as Completed\n6.Exit")
        try:
            choice= int(input("choose an option"))
        except ValueError:
            print("Invalid input.Please enter a task number.")
            continue
        choice = int(input("choose an option"))
        if choice == "1":
            user.add_task()
            continue
        elif choice == "2":
            user.view_tasks()
            continue
        elif choice == "3":
            user.edit_task()
            continue
        elif choice == "4":
            user.delete_task()
            continue
        elif choice == "5":
            user.mark_completed()
            continue
        if choice == "6":
            break
open_program()
while program:
    print("1.Profile\n2.Water Tracker\n3.Sleep Tracker\n4.Mood Tracker\n5.Activity\n6.Appointment\n7.Medicines\n8.Report\n9.Dashboard\n10.Calories\n11.my goals\n12.To Do\n13.Close Program")
    option=input("Enter your choice")
    if  option=="1":
        profile()
    elif option=="2":
        water()
    elif option=="3":
        sleep()
    elif option=="4":
        mood()
    elif option=="5":
        activity()
    elif option=="6":
        appointments_menu(appointment_manager, user_id) #-------------
    elif option=="7":
        medicines_menu(medicine_manager, user_id) #------------------
    elif option=="8":
        report(user_id)
    elif option=="9":
        dashboard = DashBoard()
        dashboard.show_dashboard(user_id)
    elif option == "10":
        calories()
    elif option=="11":
        goals()
    elif option=="12":
         to_do()              
    elif option=="13":
        break
    else:
        print("Invalid")



