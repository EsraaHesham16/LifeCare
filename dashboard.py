import json


class DashBoard:

    def get_user(self,user_id):
        with open("users.json","r") as file:
            users=json.load(file)

        return users.get(str(user_id ))

        #for user in users :
         #   if user["user_id"]==user_id :
          #      return user
        #return None

    def get_water(self,user_id):
        with open("water.json","r")as file:
            data=json.load(file)

        for water in data:
            if water["user_id"]==user_id:
                return water
        return None

    def get_sleep(self,user_id):
        with open("sleep.json","r")as file:
            data=json.load(file)

        for sleep in data:
            if sleep["user_id"]==user_id:
                return sleep
        return None

    def get_activity(self,user_id):
        with open("activity.json","r")as file:
            data=json.load(file)

        for activity in data:
            if activity ["user_id"]==user_id:
                return activity
        return None

    def get_mood(self,user_id):
        with open("mood.json","r")as file:
            data=json.load(file)

        for mood in data:
            if mood["user_id"]==user_id:
                return mood
        return None

    def get_goals(self,user_id):
        with open("goals.json","r")as file:
            goals=json.load(file)

        for goal in goals:
            if goal["user_id"]==user_id:
                return goal
        return None

    def get_medicine(self,user_id):
        with open("medicine.json","r")as file:
            medicine=json.load(file)

        taken=0
        total=0
        for med in medicine :
            if med["user_id"]==user_id :
                total+=1
                if med["taken"]:
                    taken +=1
        return taken ,total
        


    def get_appointment(self,user_id):
        with open("appointments.json","r")as file:
            appointments=json.load(file)
        for app in  appointments :
            if app["user_id"]==user_id :
                return app


    def show_dashboard(self,user_id):
        user=self.get_user(user_id )
        water = self.get_water(user_id)
        sleep = self.get_sleep(user_id)
        activity = self.get_activity(user_id)
        mood = self.get_mood(user_id)
        goals=self.get_goals(user_id)
        taken,total=self.get_medicine(user_id)
        appointment=self.get_appointment(user_id)
        if user is None:
            print("user not found")
            return
        print("\n==========Dashboard========\n")
        print("welcome:", user["name"])

        print()

        print(f"water: {water["cups"]} / {goals ['water_goal']} cups")
        print(f"sleep: {sleep["hours"]} hours")
        print(f"steps: {activity["steps"]}/{goals['steps_goal']} steps")
        print(f"mood: {mood["mood"]} ")
        print(f"medicine:{taken} /{total }")
        print(f"appointments: {appointment["title"]} - {appointment["date"]}")

    #main
    """
    from dashboard import DashBoard
    dashboard=DashBoard ()
    dashboard.show_dashboard(1)
    """

