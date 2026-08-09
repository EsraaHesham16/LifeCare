import json
from datetime import datetime , timedelta,date
class Reports:
    def show_badges(self,water,sleep,steps,mood,score,report_type):
        if report_type=="daily" or report_type=="weekly":
            if water >=8:
                print("water master")
            if sleep>=8:
                print("sleep hero")
            if steps >=8000:
                print("step champion")
            if mood=="happy" or mood=="excited":
                print("positive mood")
            if score==100:
                print("healthy day")
            if score>=80:
                print("healthy life style")
        else:
            if water >=56:
                print("water master")
            if sleep>=56:
                print("sleep hero")
            if steps >=56000:
                print("step champion")
            if mood=="happy" or mood=="excited":
                print("positive mood")
            if score==100:
                print("healthy day")
            if score>=80:
                print("healthy life style")


    def mood_score(self,mood):
        mood_points={
        "happy":25,
        "excited":25,
        "relaxed":20,
        "normal":15,
        "tired":10,
        "stressed":5,
        "sad":0
        }
        return mood_points.get(mood.lower(),0)

    def calculate_health_score(self,water,sleep,steps,mood):
        score=0
        if water>=8:
            score+=25
        if sleep>=8:
            score+=25
        if steps>=8000:
            score+=25

        score+=self.mood_score(mood)
        return score

    def overall_status(self,score):
        if score>=80:
            return"excellent"
        elif score>=60:
            return"good"
        else:
            return "improve your self!"
    def show_challenges(self,water,sleep,steps):
        print("\nchallenges")
        if water>= 8:
            print("water challenge done")
        else:
            print("drink more water!")
        if sleep >= 8:
            print("sleep challenge done")
        else:
            print("sleep more!")
        if steps >= 8000:
            print("activity challenge done")
        else:
            print("walk more!")

    def daily_report(self,user_id):
        with open("water.json","r")as file:
            water=json.load(file)
        with open("sleep.json","r")as file:
            sleep=json.load(file)
        with open("activity.json","r")as file:
            activity=json.load(file)
        with open("mood.json","r")as file:
            mood=json.load(file)
        with open("medicine.json","r")as file:
            medicine=json.load(file)
        with open("appointment.json","r")as file:
            appointments=json.load(file)

        print("\n========DAILY REPORT\n========")
        today = str(datetime.now().date())
        water_cups=0
        sleep_hours=0
        steps=0

        water_found=False
        for i in water:
            if i["user_id"]==user_id and i["date"] == today:
                water_found=True
                water_cups=i["cups"]
                print(f"water:{water_cups} cups")
        if not water_found :
            print("no water data ")


        sleep_found=False
        for i in sleep:
            if i["user_id"]==user_id and i["date"] == today:
                sleep_found=True
                sleep_hours=i["hours"]
                print(f"sleep:{sleep_hours } hours")
        if not sleep_found:
            print("no sleep data ")

        activity_found=False
        for i in activity :
            if i["user_id"]==user_id and i["date"] == today:
                activity_found=True
                steps=i["steps"]
                print(f"steps:{steps} ")

        if not activity_found:
            print("no activity data ")

        mood_found=False
        mood_status=""
        for i in mood:
            if i["user_id"]==user_id and i["date"] == today:
                mood_found=True
                mood_status=i["mood"]
                print(f"mood: {mood_status }")
        if not mood_found:
            print("no mood data ")

        print("\nMEDICINE")
        if not medicine :
            print("no medicine data available")
        else:
            today=datetime .today().strftime("%Y-%m-%d")
            found =False
            
            for i in medicine :
                if i ["user_id"]==user_id:
                    found=True
                    print(f"{i['medicine_name']} - {i['dose']}")

                    if today in i["taken"]:
                        for j in range(len(i["times"])):
                            time=i["times"][j]
                            status=i["taken"][today][j]

                            if status :
                                print(f"{time} :taken")
                            else:
                                print(f"{time} :missed")
                    else:
                         print("no doses recorded tody")
            if not found:
                print("no medicine data for this user")


        print("\nAppointments")
        if not appointments:
            print("no appointment data available")
        else:
            today = datetime.today().strftime("%Y-%m-%d")
            found=False
            for i in appointments :
                if i["user_id"] == user_id and i["date"]==today :
                    found=True
                    print(f"title :{i['title']}")
                    print(f"doctor:{i['doctor']}")
                    print(f"clinic:{i['clinic']}")
                    print(f"date :{i['date']}")
                    print(f"time:{i['time']}")
                    print(f"status :{i['status']}")
                    print(f"notes :{i['notes']}")

            if not found:
                print("no appointments found")


        score=self.calculate_health_score(water_cups,sleep_hours,steps,mood_status )

        print(f"\n health score:{score} /100")
        self.show_challenges(water_cups,sleep_hours,steps )
        self.show_badges(water_cups,sleep_hours,steps,mood_status,score,"daily")

        print(f"\n overall status: {self.overall_status(score)}")


    def weekly_report(self,user_id):
        with open("water.json","r")as file:
            water=json.load(file)
        with open("sleep.json","r")as file:
            sleep=json.load(file)
        with open("activity.json","r")as file:
            activity=json.load(file)
        with open("mood.json","r")as file:
            mood=json.load(file)
        with open("medicine.json","r")as file:
            medicine=json.load(file)
        with open("appointment.json","r")as file:
            appointments=json.load(file)

        print("\n========WEEKLY REPORT========\n")

        total_water=0
        total_sleep=0
        total_steps=0
        water_days=0
        sleep_days=0
        activity_days=0
        moods = {
            "happy": 0,
            "excited": 0,
            "relaxed": 0,
            "normal": 0,
            "tired": 0,
            "stressed": 0,
            "sad": 0
        }
        taken=0
        missed=0
        appointment_count=0
        today = datetime.today()
        week_ago = today - timedelta(days=7)

        for i in water:
            record_data = datetime.strptime(i["date"], "%Y-%m-%d")
            if i ["user_id"]==user_id and record_data>=week_ago :
                total_water+=i["cups"]
                water_days+=1
        average_water=total_water / water_days if water_days>0 else 0
        print(f"average water:{average_water } cups")

        for i in sleep:
            record_data = datetime.strptime(i["date"], "%Y-%m-%d")
            if i["user_id"] == user_id and record_data>=week_ago :
                total_sleep  += i["hours"]
                sleep_days += 1
        average_sleep = total_sleep / sleep_days if sleep_days>0 else 0
        print(f"average sleep:{average_sleep} hours")

        for i in activity :
            record_data = datetime.strptime(i["date"], "%Y-%m-%d")
            if i["user_id"] == user_id and record_data>=week_ago :
                total_steps  += i["steps"]
                activity_days+= 1
        average_steps = total_steps / activity_days if activity_days >0 else 0
        print(f"average steps:{average_steps} ")

        for i in mood:
            record_data = datetime.strptime(i["date"], "%Y-%m-%d")
            if i["user_id"]==user_id and record_data>=week_ago :
                mood_status=i["mood"].lower()
                if mood_status in moods :
                    moods[mood_status]+=1
        print("\n mood summary")
        for mood_status, count in moods.items():
            print(f"{mood_status}: {count}")

        mood_result=max(moods,key=moods.get)
        print(f"overall mood: {mood_result }")

        for i in medicine:
            if i["user_id"] == user_id:
                for date,doses in i["taken"].items():

                   record_data = datetime.strptime(date, "%Y-%m-%d")

                   if record_data>=week_ago :
                       for dose in doses:
                           if dose :
                               taken+=1
                           else:
                               missed+=1

        print("\nMedicine Summary")
        if taken==0 and missed==0:
           print("no medicine data available")
        else:
            print(f"taken: {taken}")
            print(f"missed: {missed}")


        for i in appointments :
            record_data = datetime.strptime(i["date"], "%Y-%m-%d")
            if i["user_id"] == user_id and record_data>=week_ago :

                appointment_count+=1

                print(f"\ntitle :{i['title']}")
                print(f"doctor:{i['doctor']}")
                print(f"clinic:{i['clinic']}")
                print(f"date :{i['date']}")
                print(f"time:{i['time']}")
                print(f"status :{i['status']}")
                print(f"notes :{i['notes']}")

            if appointment_count==0:
                print("no appointments available")
            else:
                print(f"total appointments: {appointment_count}")



        score=self.calculate_health_score(average_water,average_sleep,average_steps ,mood_result )

        print(f"\nhealth score: {score} /100")
        self.show_challenges(average_water,average_sleep,average_steps )
        self.show_badges(average_water,average_sleep,average_steps ,mood_result,score,"weekly")

        print(f"\n overall status: {self.overall_status(score)}")


    def calculate_monthly_score(self,water,sleep,steps,mood):
        score=0

        if water>=56:
             score+=25
        if sleep>=56:
             score+=25
        if steps>=56000:
             score+=25
        score += self.mood_score(mood)
        return score


    def show_monthly_challenges(self,water,sleep,steps):
        print("\nchallenges")
        if water >= 56:
            print("water challenge done")
        else:
            print("drink more water!")
        if sleep >= 56:
            print("sleep challenge done")
        else:
            print("sleep more!")
        if steps >= 56000:
            print("activity challenge done")
        else:
            print("walk more!")

    def monthly_report(self,user_id):
        with open("water.json", "r") as file:
            water = json.load(file)
        with open("sleep.json", "r") as file:
            sleep = json.load(file)
        with open("activity.json", "r") as file:
            activity = json.load(file)
        with open("mood.json","r")as file:
            mood=json.load(file)
        with open("medicine.json","r")as file:
            medicine=json.load(file)
        with open("appointment.json","r")as file:
            appointments=json.load(file)

        print("\n========MONTHLY REPORT========\n")

        total_water=0
        total_sleep = 0
        total_steps = 0
        moods = {
            "happy": 0,
            "excited": 0,
            "relaxed": 0,
            "normal": 0,
            "tired": 0,
            "stressed": 0,
            "sad": 0
        }
        taken = 0
        missed = 0
        appointment_count = 0
        today=datetime.today()

        for i in water:
            record_data = datetime.strptime(i["date"], "%Y-%m-%d")
            if i ["user_id"]==user_id and record_data.month ==today.month and record_data.year==today.year :
                total_water+=i["cups"]
        print(f"total water: {total_water} cups")

        for i in sleep:
            record_data = datetime.strptime(i["date"], "%Y-%m-%d")
            if i["user_id"] == user_id and record_data.month ==today.month and record_data.year==today.year:
                total_sleep  += i["hours"]
        print(f"total sleep: {total_sleep} hours")


        for i in activity :
            record_data = datetime.strptime(i["date"], "%Y-%m-%d")
            if i["user_id"] == user_id and record_data.month ==today.month and record_data.year==today.year:
                total_steps  += i["steps"]
        print(f"total steps: {total_steps}")

        for i in mood:
            record_data = datetime.strptime(i["date"], "%Y-%m-%d")
            if i["user_id"]==user_id and record_data.month ==today.month and record_data.year==today.year :
                mood_status = i["mood"].lower()
                if mood_status in moods:
                    moods[mood_status] += 1
        print("\n mood summary")
        for mood_status, count in moods.items():
            print(f"{mood_status}: {count}")

        mood_result = max(moods, key=moods.get)
        print(f"overall mood: {mood_result}")

        for i in medicine:
            if i["user_id"] == user_id:
                for date, doses in i["taken"].items():
                    record_data = datetime.strptime(date, "%Y-%m-%d")

                    if record_data.month ==today.month and record_data.year==today.year:
                        for dose in doses:
                             if dose:
                                 taken += 1
                             else:
                                 missed += 1

        print("\nMedicine Summary")
        if taken==0 and missed==0:
           print("no medicine data available")
        else:
            print(f"taken: {taken}")
            print(f"missed: {missed}")

        for i in appointments :
            record_data = datetime.strptime(i["date"], "%Y-%m-%d")
            if i["user_id"] == user_id and record_data.month ==today.month and record_data.year==today.year:
                appointment_count+=1

                print(f"title :{i['title']}")
                print(f"doctor:{i['doctor']}")
                print(f"clinic:{i['clinic']}")
                print(f"date :{i['date']}")
                print(f"time:{i['time']}")
                print(f"status :{i['status']}")
                print(f"notes :{i['notes']}")

            if appointment_count==0:
                print("no appointments available")
            else:
                print(f"total appointments: {appointment_count}")


        # score=self.calculate_health_score(total_water,total_sleep ,total_steps )

        score = self.calculate_monthly_score(total_water, total_sleep, total_steps,mood_result )

        print(f"\n health score:{score} /100")
        self.show_monthly_challenges(total_water,total_sleep,total_steps )
        self.show_badges(total_water , total_sleep , total_steps , mood_result, score, "monthly")

        print(f"\n overall status: {self.overall_status(score)}")