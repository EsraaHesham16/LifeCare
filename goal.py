import json

class Goals:
    def menu(self,user_id):
        with open("goals.json","r") as file:
            goals=json.load(file)

        user_goal= None
        for goal in goals:
            if goal["user_id"]==user_id:
                user_goal=goal
                break
        if user_goal is None:
            user_goal={
                "user_id": user_id,
                "water_goal": 8,
                "steps_goal": 8000
            }
            goals.append(user_goal )

            with open("goals.json","r") as file:
                json.dump(goals, file, indent=4)

        print("\n==========MY GOALS==========")
        print("current goals: ")
        print(f"water: {user_goal["water_goal"]} cups")
        print(f"steps: {user_goal["steps_goal"]} ")

        print("\n1. keep current goals")
        print("2. change goals")
        print("3. back")

        choice=input("enter your choice: ")

        if choice=="1":
            print("current goal kept")
        elif choice=="2":
            self.change_goals(user_id)
        elif choice=="3":
            return
        else:
            print("invalid choice")

    def change_goals(self,user_id):
        with open("goals.json","r") as file:
            goals=json.load(file)

        for goal in goals:
            if goal["user_id"]==user_id:
                goal["water_goal"] = int(input("enter new water goal:"))
                goal["steps_goal"] = int(input("enter new steps goal:"))
                break

        with open("goals.json","w") as file:
            json.dump(goals,file, indent=4)

        print("goals updated successfully!")
"""
#main
from goals import Goals
goals=Goals()
elif choise=="7":
    goals.menu(user_id ) 
"""
