import json
from datetime import datetime

class ActivityTracker:
    def __init__(self, user_id):
        self.user_id=user_id
        try:
            with open("activity.json","r") as file:
                self.content=json.load(file)

        except:
            with open("activity.json","w") as file:
                self.content=[]
                json.dump(self.content,file)


    def add_activity(self):
        date = str(datetime.now().date())
        today = 0
        for user in self.content:
            if user.get("date") == date and user.get("user_id") == self.user_id:
                today = 1
        if today == 1:
            print("you added yor activity for today.")
        else:
            try:
                steps=int(input("enter steps for today: "))
                duration=int(input("enter exercise duration (by min): "))
                if steps<0 or duration<0:
                    print("values can't be negative")
                    redo=input("want to try again? (y/n) ")
                    if redo=="y":
                        ActivityTracker.add_activity(self)
                    else:
                        return
                else:
                    activity={
                        "user_id":self.user_id,
                        "date": date,
                        "steps": steps,
                        "duration": duration
                    }
                    self.content.append(activity)
                    with open("activity.json", "w") as file:
                        json.dump(self.content, file, indent=4)
                    print("activity added")
            except:
                print("you enter invalid inputs\nplease make sure you enter a numbers")
                redo=input("want to try again?(y/n) ").strip().lower()
                if redo=="y":
                    ActivityTracker.add_activity(self)

    def view_today_activity(self):
        date = str(datetime.now().date())
        today = 0
        for user in self.content:
            if user.get("date") == date and user.get("user_id") == self.user_id:
                print(f'your steps for today : {user["steps"]}')
                print(f'your exercise duration for today : {user["duration"]}')
                today = 1
        if today == 0:
            print("you didn't add activity for today yet.")
            add = input("want to add? (y/n) ").strip().lower()
            if add == "y":
                ActivityTracker.add_activity(self)

    def delete_activity(self):
        while True:
            delete_date=input("enter date to delete (year-month-day): ")
            day = 0
            for user in self.content:
                if user.get("date") == delete_date and user.get("user_id") == self.user_id:

                    self.content.remove(user)
                    with open("activity.json", "w") as file:
                        json.dump(self.content, file, indent=4)
                    print("date deleted")
                    day = 1
            if day==1:
                break
            else:
                print("invalid date!\nplease make sure you enter right date\n(ex:2026-08-06)")
                redo=input("want to try again? (y/n): ")
                if redo=="y":
                    continue
                else:
                    break
    
    def edit_activity(self):
        try:
            edit_steps = int(input("enter edited steps: "))
            edit_duration = int(input("enter edited exercise duration (by min): "))
            if edit_steps < 0 or edit_duration < 0:
                print("values can't be negative")
                redo = input("want to try again? (y/n) ")
                if redo == "y":
                    ActivityTracker.edit_activity(self)
                else:
                    return
            else:
                while True:
                    edit_date = input("enter date to edit (year-month-day): ")
                    day = 0
                    for user in self.content:
                        if user.get("date") == edit_date and user.get("user_id") == self.user_id:
                            user["steps"] = edit_steps
                            user["duration"]= edit_duration
                            with open("activity.json", "w") as file:
                                json.dump(self.content, file, indent=4)
                            print("activity edited")
                            day = 1
                            return
                    if day == 0:
                        print("invalid date!\nplease make sure you enter right date\n(ex:2026-08-06)")
                        redo = input("want to try again? (y/n): ")
                        if redo == "y":
                            continue
                        else:
                            break
        except:
            print("you enter invalid inputs\nplease make sure you enter a numbers")
            redo = input("want to try again?(y/n) ").strip().lower()
            if redo == "y":
                ActivityTracker.edit_activity(self)

    def streak(self):
        streak=1
        date1=datetime.now().date()
        dates=[]
        for user in self.content:
            if user["user_id"]==self.user_id:
                dates.append(user["date"])
        dates.sort(reverse=True)
        if len(dates)==0:
            streak=0
        else:
            if dates[0]==str(date1):
                dates.pop(0)
            for date in dates:
                date=str(date)
                date2=datetime.strptime(date,"%Y-%m-%d").date()
                if (date1-date2).days==1:
                    streak+=1
                    date1=date2
                else:
                    break
        print(f'Current activity streak : {streak}')
        print("keep tracking your activity streak every day!")

    def get_by_date(self):
        while True:
            get_date=input("enter date to get your activity (year-month-day): ")
            day = 0
            for user in self.content:
                if user.get("date") == get_date and user.get("user_id") == self.user_id:
                    print(f'your steps in {get_date} is {user["steps"]} step')
                    print(f'your exercise duration is {user["duration"]} min')
                    day=1
                    edit=input("want to edit your activity in that day? (y/n) ").strip().lower()
                    if edit=="y":
                        while True:
                            try:
                                edit_steps = int(input("enter edited steps: "))
                                edit_duration = int(input("enter edited exercise duration (by min): "))
                                if edit_steps < 0 or edit_duration < 0:
                                    print("values can't be negative")
                                    redo = input("want to try again? (y/n) ")
                                    if redo == "y":
                                        continue
                                    else:
                                        return
                                else:
                                    user["steps"] = edit_steps
                                    user["duration"] = edit_duration
                                    with open("activity.json", "w") as file:
                                        json.dump(self.content, file, indent=4)
                                    print("activity edited")
                                    return
                            except:
                                print("you enter invalid inputs\nplease make sure you enter a numbers")
                                redo = input("want to try again?(y/n) ").strip().lower()
                                if redo == "y":
                                    continue
                                else:
                                    return
                    else:
                        return
            if day==0:
                print("invalid date!\nplease make sure you enter right date\n(ex:2026-08-06)\nor may this day is not added")
                redo=input("want to try again? (y/n): ")
                if redo=="y":
                    continue
                else:
                    return


# activity=ActivityTracker(1)
# activity.add_activity()
# activity.streak()
# while True:
#     activity=ActivityTracker(user_id)
#     print("1.add activity\n2.view today activity\n3.delete activity by date\n4.edit activity by date\n5.streak of activity\n6.get activity by date\n7.back")
#     activity_choice=input("choose number: ")
#     if activity_choice=="1":
#         activity.add_activity()
#     elif activity_choice=="2":
#         activity.view_today_activity()
#     elif activity_choice=="3":
#         activity.delete_activity()
#     elif activity_choice=="4":
#         activity.edit_activity()
#     elif activity_choice=="5":
#         activity.streak()
#     elif activity_choice=="6":
#         activity.get_by_date()
#     elif activity_choice=="7":
#         break
#     else:
#         print("invalid input!\ntry again.")
