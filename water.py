import json
import random
from datetime import date,timedelta,datetime
good_water_messages = [
    "Good job! Keep drinking water regularly 💧",
    "You are doing well. Keep maintaining this habit!",
    "Nice progress! You are getting closer to your goal.",
    "Great work! Your hydration level is improving.",
    "Keep it up! A few more cups to reach your goal."
]
low_water_messages = [
    "You need to drink more water today. Stay hydrated 💧",
    "Your water intake is low. Try to drink another cup.",
    "Don't forget to drink water regularly throughout the day.",
    "Your body needs more water. Keep going!",
    "A little more water can improve your energy and focus.",
    "You are below your daily goal. Try to drink more water."
]

def load_water():
    try:
        with open("water.json") as file:
            return json.load(file)

    except FileNotFoundError:
        return []


def save_water(data):
    with open("water.json","w") as file:
        json.dump(data,file,indent=4)

class WaterTracker:
    def __init__(self,user_id):
        self.user_id = user_id
        self.today = str(date.today())
        self.data = load_water()

    def add_cup(self):
        found = False
        for record in self.data:
            if record["user_id"] == self.user_id and record["date"] == self.today:
                record["cups"] +=1
                found = True
                break
        if found == False:
            new_record = {
                "user_id" :self.user_id,
                "date" : self.today,
                "cups" : 1,
                "goal" : 8
            }
            self.data.append(new_record)
        save_water(self.data)
        print("Added successfully")
    def calculate_water_streak(self):
        user_water = []
        for record in self.data:
            if record["user_id"] == self.user_id:
                user_water.append(record)
        if len(user_water) == 0:
            return 0
        user_water.sort(key=lambda x: x["date"], reverse=True)
        streak = 0
        expected_day = date.today()
        for record in user_water:
            record_date = datetime.strptime(record["date"], "%Y-%m-%d").date()
            if record_date == expected_day:
                if record["cups"] >=8:
                    streak += 1
                    expected_day -= timedelta(days=1)
                else:
                    break
            else:
                break
        return streak
    def view_today_water(self):
        found = 0
        print("======== Today's Water ==========")
        for record in self.data:
            if record["user_id"] == self.user_id and record["date"] == self.today:
                print(f"💧 You drank {record["cups"]} / {record["goal"]} ")
                progress = round((record["cups"] / record["goal"]) * 100)
                print(f"📊 Progress: {progress}%")
                print(f"\n🔥 Streak: {self.calculate_water_streak()}")
                if progress == 100:
                    print("🎉 Status: Goal Completed")
                    print("💡 Advice:\nNice progress! You are getting closer to your goal.")
                elif progress >= 50:
                    print("✅ Status: Good Hydration")
                    print(f"💡 Advice:\n{random.choice(good_water_messages)}")
                else:
                    print("⚠️ Status: Low Hydration")
                    print(f"💡 Advice:\n{random.choice(low_water_messages)}")

                found = 1
                break
        if found == 0:
            choose = int(input("You do not enter any cup today. Do you want to add cup?(1.yes / 2.no)"))
            if choose == 1:
                self.add_cup()

    def view_history(self):
        found = 0
        for record in self.data:
            if record["user_id"] == self.user_id:
                print(f"{record["date"]} : {record["cups"]}")
                found = 1
        if found == 0:
            print("There is no any history yet!")
    def get_today_water(self):
        for record in self.data:
            if record["user_id"] == self.user_id and record["date"] == self.today:
                return {
                    "cups" : record["cups"],
                    "goal" : record["goal"]
                }
        return {
                    "cups" : 0,
                    "goal" :8
                }
    def get_water_progress(self):
        data = self.get_today_water()
        progress = (data["cups"] / data["goal"]) * 100
        return round(progress,2)

    def get_water_history(self):
        history = []
        for record in self.data:
            if record["user_id"] == self.user_id:
                history.append(record)
        return history

# user_id = int(input("enter your id: "))
# person = WaterTracker(user_id)
# print("========= Water Tracker ===========")
# print("Today's Goal: 8")
# while True:
#     option = int(input("1.Add cup\n2.View today's water\n3.View history water\n4.back"))
#     if option == 1:
#         person.add_cup()
#     elif option == 2:
#         person.view_today_water()
#     elif option == 3:
#         person.view_history()
#     elif option == 4:
#         break
#     else:
#         print("invalid option\nPlease enter(1,2,3): ")
#     press = input("press enter to continue")