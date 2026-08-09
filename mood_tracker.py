import json
from datetime import datetime

class MoodTracker:
    def __init__(self, user_id):
        self.user_id=user_id
        try:
            with open("mood.json", "r") as file:
                self.content = json.load(file)

        except:
            with open("mood.json", "w") as file:
                self.content = []
                json.dump(self.content, file)

    def add_mood(self):
        date = str(datetime.now().date())
        today = 0
        for user in self.content:
            if user.get("date") == date and user.get("user_id") == self.user_id:
                today = 1
        if today == 1:
            print("you added yor mood for today.")
        else:
            while True:
                user_mood = input("what is your mood today?\n( happy / normal / sad / angry / tired / stressed / excited ) ").strip().lower()
                if user_mood not in ["happy","normal","sad","angry","tired","stressed","excited"]:
                    print('invalid input')
                    redo=input("want to try again? (y/n) ")
                    if redo=="y":
                        continue
                    else:
                        break
                else:
                    mood = {
                        "user_id": self.user_id,
                        "date": date,
                        "mood": user_mood
                    }
                    self.content.append(mood)
                    with open("mood.json", "w") as file:
                        json.dump(self.content, file, indent=4)
                    print("mood added")
                    break

    def view_today_mood(self):
        date = str(datetime.now().date())
        today=0
        for user in self.content:
            if user.get("date")== date and user.get("user_id") == self.user_id:
                print(f'your mood for today : {user["mood"]}')
                today=1
        if today==0:
            print("you didn't add mood for today yet.")
            add=input("want to add? (y/n) ").lower()
            if add=="y":
                MoodTracker.add_mood(self)

    def delete_mood(self):
        while True:
            delete_date=input("enter date to delete (year-month-day): ")
            day = 0
            for user in self.content:
                if user.get("date") == delete_date and user.get("user_id") == self.user_id:
                    self.content.remove(user)
                    with open("mood.json", "w") as file:
                        json.dump(self.content, file, indent=4)
                    print("date deleted")
                    day = 1
                    return
            if day==0:
                print("invalid date!\nplease make sure you enter right date\n(ex:2026-08-06)")
                redo=input("want to try again? (y/n): ")
                if redo=="y":
                    continue
                else:
                    break

    def edit_mood(self):
        while True:
            edited_mood = input("what is your new mood?\n( happy / normal / sad / angry / tired / stressed / excited ) ").strip().lower()
            if edited_mood not in ["happy", "normal", "sad", "angry", "tired","stressed","excited"]:
                print('invalid input')
                redo = input("want to try again? (y/n) ")
                if redo == "y":
                    continue
                else:
                    break
            edit_date = input("enter date to edit (year-month-day): ")
            day = 0
            for user in self.content:
                if user.get("date") == edit_date and user.get("user_id") == self.user_id:
                    user["mood"]=edited_mood
                    with open("mood.json", "w") as file:
                        json.dump(self.content, file, indent=4)
                    print("date edited")
                    day = 1
                    return
            if day==0:
                print("invalid date!\nplease make sure you enter right date\n(ex:2026-08-06)")
                redo=input("want to try again? (y/n): ")
                if redo=="y":
                    continue
                else:
                    break

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
        print(f'Current mood streak : {streak}')
        print("keep tracking your mood streak every day!")

    def get_by_date(self):
        while True:
            get_date=input("enter date to get your mood (year-month-day): ")
            day = 0
            for user in self.content:
                if user.get("date") == get_date and user.get("user_id") == self.user_id:
                    print(f'your mood in {get_date} is {user["mood"]}')
                    day=1
                    edit=input("want to edit your mood in that day? (y/n) ").strip().lower()
                    if edit=="y":
                        while True:
                            edited_mood = input("what is your new mood?\n( happy / normal / sad / angry / tired / stressed / excited ) ").strip().lower()
                            if edited_mood not in ["happy", "normal", "sad", "angry", "tired","stressed","excited"]:
                                print('invalid input')
                                redo = input("want to try again? (y/n) ")
                                if redo == "y":
                                    continue
                                else:
                                    break
                            user["mood"]=edited_mood
                            with open("mood.json", "w") as file:
                                json.dump(self.content, file, indent=4)
                            print("date edited")
                            return
                    else:
                        return
            if day==0:
                print("invalid date!\nplease make sure you enter right date\n(ex:2026-08-06)\nor may this day is not added")
                redo=input("want to try again? (y/n): ")
                if redo=="y":
                    continue
                else:
                    break

# mood=MoodTracker(1)
# mood.streak()
# while True:
#     mood=MoodTracker(user_id)
#     print("1.add mood\n2.view today mood\n3.delete mood by date\n4.edit mood by date\n5.streak of mood\n6.get mood by date\n7.back")
#     mood_choice = input("choose number: ")
#     if mood_choice == "1":
#         mood.add_mood()
#     elif mood_choice == "2":
#         mood.view_today_mood()
#     elif mood_choice == "3":
#         mood.delete_mood()
#     elif mood_choice == "4":
#         mood.edit_mood()
#     elif mood_choice == "5":
#         mood.streak()
#     elif mood_choice == "6":
#         mood.get_by_date()
#     elif mood_choice == "7":
#         break
#     else:
#         print("invalid input!\ntry again.")