import json
import random
from datetime import date,datetime,timedelta

low_sleep_messages = [
    "You need more sleep. Try to sleep earlier tonight 😴",
    "Your sleep duration is low. Give your body more time to rest.",
    "A good night's sleep helps you stay focused and energetic.",
    "Try to get enough sleep to improve your mood and productivity.",
    "Your body needs recovery. Aim for more sleeping hours.",
    "Sleeping less can affect your energy. Try to create a better sleep routine.",
    "Don't forget to take care of your rest as much as your daily tasks.",
    "You slept less than recommended. Try to relax and sleep earlier today."
]
good_sleep_messages = [
    "Great job! You are getting a healthy amount of sleep 😴✨",
    "Excellent! Keep maintaining your good sleep habits.",
    "Your sleep schedule looks good. Keep it up!",
    "A good sleep routine helps you stay active and focused.",
    "Well done! Your body is getting the rest it needs.",
    "Keep this healthy sleep pattern going!"
]
high_sleep_messages = [
    "You slept longer than usual. Try to keep a balanced sleep schedule.",
    "Too much sleep can sometimes make you feel tired. Keep your routine balanced.",
    "Your sleep duration is high today. Listen to your body and maintain a healthy routine.",
    "Long sleep is okay sometimes, but consistency is important.",
    "Try to maintain a regular sleep schedule for better energy."
]
def load_sleep():
    try:
        with open("sleep.json") as file:
            return json.load(file)

    except FileNotFoundError:
        return []


def save_sleep(data):
    with open("sleep.json","w") as file:
        json.dump(data,file,indent=4)

class SleepTracker:
    def __init__(self,user_id):
        self.user_id = user_id
        self.data = load_sleep()
        self.today = str(date.today())
        self.goal = 8
        self.hours = 0
    def add_sleep(self):
        found = 0
        for record in self.data:
            if record["user_id"] == self.user_id and record["date"] == self.today:
                found = 1
                self.hours = record["hours"]
                print("Sleep record already exist for today!")
                break
        if found == 0:
            while True:
                sleep_time = input("Enter sleep time: ")
                wake_time = input("Enter wake time: ")
                if sleep_time == wake_time:
                    print("Invalidation sleep. The sleep time equal wake time try enter again")
                else:
                    break
            while True:
                quality_num = int(input("Sleep Quality:\n1.Excellent\n2.Good\n3.Bad\n"))
                if quality_num == 1:
                    quality = "Excellent"
                    break
                elif quality_num == 2:
                    quality = "Good"
                    break
                elif quality_num == 3:
                    quality = "Bad"
                    break
                else:
                    print("Invalid input enter (1, 2, 3): ")
            sleep = datetime.strptime(sleep_time, "%H:%M")
            wake = datetime.strptime(wake_time, "%H:%M")
            if wake < sleep:
                wake += timedelta(days=1)
            duration = wake - sleep
            hours = duration.total_seconds() / 3600
            self.hours = round(hours, 2)
            new_data = {
                "user_id": self.user_id,
                "date": self.today,
                "hours": self.hours,
                "quality" : quality,
                "goal": self.goal
            }
            self.data.append(new_data)
        save_sleep(self.data)

    def calculate_sleep_streak(self):
        user_sleep = []
        for record in self.data:
            if record["user_id"] == self.user_id:
                user_sleep.append(record)
        if len(user_sleep) == 0:
            return 0
        user_sleep.sort(key=lambda x: x["date"],reverse=True)
        streak = 0
        expected_day = date.today()
        for record in user_sleep:
            record_date = datetime.strptime(record["date"],"%Y-%m-%d").date()
            if record_date == expected_day:
                if record["hours"] >= 7:
                    streak += 1
                    expected_day -= timedelta(days=1)
                else:
                    break
            else:
                break
        return streak
    def view_today_sleep(self):
        print("========== Today's Sleep ========\n")
        print("Goal: 8 Hours\n")

        found = False
        for record in self.data:
            if record["user_id"] == self.user_id and record["date"] == self.today:
                print(f"Sleep duration: {record["hours"]} hours\n")
                print(f"Sleep Quality : {record["quality"]}")
                print(f"\n🔥 Streak: {self.calculate_sleep_streak()}")
                self.hours = record["hours"]
                if self.hours < 6:
                    print("\nStatus : ⚠️ Poor Sleep\n")
                    print(random.choice(low_sleep_messages))
                elif self.hours < 9:
                    print("\nStatus : ✅ Healthy Sleep\n")
                    print(random.choice(good_sleep_messages))
                else:
                    print("\nStatus : 💤 Long Sleep\n")
                    print(random.choice(high_sleep_messages))
                found = not found
                break
        if found == False:
            choice = int(input("You do not entered your sleep time! do you want to enter it(1.yes / 2.no)"))
            if choice == 1:
                self.add_sleep()
    def view_Sleep_history(self):
        print("========= History ==========")
        found = 0
        for record in self.data:
            if record["user_id"] == self.user_id:
                print(f"{record["date"]} : {record["hours"]}")
                found = 1
        if found == 0:
            print("There is no history. You did not add any sleep before!")


# user_id = int(input("enter id: "))
# person = SleepTracker(user_id)
# print("========= Sleep Tracker =============")
# while True:
#     option = int(input("1.Add Today's Sleep\n2.View Today's Sleep\n3.View Sleep History\n4.back"))
#     if option == 1:
#         person.add_sleep()
#     elif option == 2:
#         person.view_today_sleep()
#     elif option == 3:
#         person.view_Sleep_history()
#     elif option == 4:
#         break
#     else:
#         print("invalid option. Please enter(1, 2, 3, 4): ")
#     press = input("press enter to continue.")


