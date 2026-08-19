import json
from datetime import datetime
import random

class Calories:
    def __init__(self,user_id):
        self.user_id=user_id

        try:
            with open("calories.json", "r") as file:
                self.content = json.load(file)

        except:
            with open("calories.json", "w") as file:
                self.content = []
                json.dump(self.content, file)
        try:
            with open("users_calories.json", "r") as file:
                self.daily_calories = json.load(file)

        except:
            with open("users_calories.json", "w") as file:
                self.daily_calories = []
                json.dump(self.daily_calories, file)

    def add_data(self):
        while True:
            found = 0
            for user in self.content:
                if user.get("user_id")== self.user_id:
                    found=1
                    print("you enter your data already")
                    return
            if found ==0:
                try:
                    gender=input("what's your gender? (male/female) ").strip().lower()
                    if gender not in ["male","female"]:
                        print("invalid input!")
                        redo=input("want to try again? (y/n) ").strip().lower()
                        if redo =="y":
                            continue
                        else:
                            break
                    age=int(input("what's your age?" ))
                    if age < 18 :
                        print("you must be +18")
                        redo = input("want to try again? (y/n) ").strip().lower()
                        if redo == "y":
                            continue
                        else:
                            break
                    height=int(input("what's your height? (in cm) "))
                    if height < 50 :
                        print("height must be in cm")
                        redo = input("want to try again? (y/n) ").strip().lower()
                        if redo == "y":
                            continue
                        else:
                            break

                    weight=int(input("what's your weight? (in kg) "))
                    if weight <=0:
                        print("invalid input!")
                        redo = input("want to try again? (y/n) ").strip().lower()
                        if redo == "y":
                            continue
                        else:
                            break

                    bmi = round(weight / ((height ** 2) / 10000), 2)
                    if bmi < 18.5:
                        print(f'since you are underweight, we recommend gain weight\n')
                    elif 25 <= bmi:
                        print(f'since you are overweight, we recommend lose weight\n')
                    else:
                        print(f'we recommend maintain\n')
                    goal = input("what's your weight goal? ( maintain / lose / gain )").strip().lower()
                    if goal not in ["maintain","lose","gain"]:
                        print("invalid input!")
                        redo=input("want to try again? (y/n) ").strip().lower()
                        if redo =="y":
                            continue
                        else:
                            break

                    user_data={
                        "user_id":self.user_id,
                        "age": age,
                        "gender":gender,
                        "height":height,
                        "weight":weight,
                        "goal":goal
                    }
                    self.content.append(user_data)
                    with open("calories.json", "w") as file:
                        json.dump(self.content, file, indent=4)
                    print("data added")
                    break
                except:
                    print("invalid inputs!")
                    redo = input("want to try again? (y/n) ").strip().lower()
                    if redo == "y":
                        continue
                    else:
                        break

    def calculate_bmi(self):
        while True:
            found=0
            for user in self.content:
                if user.get("user_id")== self.user_id:
                    weight = user.get("weight")
                    height = user.get("height")
                    bmi=round(weight/((height**2)/10000),2)
                    found=1
                    if bmi < 18.5:
                        your_weight="under weight"
                    elif 18.5 <= bmi < 25 :
                        your_weight = "healthy weight"
                    elif 25 <= bmi <30:
                        your_weight= "over weight"
                    else:
                        your_weight="obesity"
                    print(f"your BMI is {bmi}")
                    print(f'you are {your_weight}')
                    if your_weight == "under weight":
                        print("we advice you to gain weight")

                    elif your_weight in ["over weight","obesity"]:
                        print("we advice you to lose weight")

                    else:
                        print("your weight is perfect!")


                    return
            if found==0:
                print("you don't enter your data yet to calculate BMI")
                enter_data=input("want to enter your data? (y/n) ").strip().lower()
                if enter_data=="y":
                    Calories.add_data(self)
                else:
                    break

    def calculate_calories(self):
        while True:
            found = 0
            for user in self.content:
                if user.get("user_id")== self.user_id:
                    found = 1
                    weight = user.get("weight")
                    height = user.get("height")
                    gender = user.get("gender")
                    age = user.get("age")
                    goal = user.get("goal")
                    active_level=int(input("rate your activity level from 0 (sedentary) to 10 (extremely active) "))
                    if 0 <= active_level <=2 :
                        factor = 1.2
                    elif active_level == 3 or active_level==4:
                        factor = 1.375
                    elif active_level == 5 or active_level ==6:
                        factor = 1.55
                    elif active_level == 7 or active_level == 8:
                        factor = 1.725
                    elif active_level == 9 or active_level == 10:
                        factor = 1.9
                    else:
                        print("invalid input")
                        continue
                    if gender == "male":
                        TDEE = int(((10 * weight) + (6.25 * height) - ( 5 * age ) - 5 ) * factor)
                    else:
                        TDEE = int(((10 * weight) + (6.25 * height) - (5 * age) - 161) * factor)
                    print(f'you need {TDEE} kcal/day to maintain')
                    if goal == "gain":
                        TDEE+=250
                        print(f'since your gaol is to gain weight, you need {TDEE} : {TDEE + 250} kcal/day')
                    elif goal == "lose":
                        TDEE-=250
                        print(f'since your gaol is to lose weight, you need {TDEE} : {TDEE - 250} kcal/day')
                    else:
                        pass
                    user["TDEE"] = TDEE

                    with open("calories.json", "w") as file:
                        json.dump(self.content, file, indent=4)
                    return
            if found == 0:
                print("you don't enter your data yet to calculate calories")
                enter_data = input("want to enter your data? (y/n) ").strip().lower()
                if enter_data == "y":
                    Calories.add_data(self)
                else:
                    break

    def progress(self):
        while True:
            today = str(datetime.now().date())
            daily=0
            id = 0
            for user in self.content:
                if user.get("user_id") == self.user_id:
                    id = 1
                    TDEE = user.get("TDEE")
                    if TDEE == None:
                        print("you don't calculate your need of calories yet ")
                        calc = input("want to calculate it? (y/n)").strip().lower()
                        if calc == "y":
                            Calories.calculate_calories(self)
                            continue
                        else:
                            return
                    else:
                        for user in self.daily_calories:
                            if user.get("user_id") == self.user_id and user.get("date") == today:
                                daily = 1
                                user_calories = user.get("calories")
                        if daily==0:
                            user_calories=0
                        needed = TDEE - user_calories
                        if needed > 0 :
                            print(f'you still need {needed} kcal')
                        elif needed <0:
                            print(f'you have exceeded your daily calorie limit by {-1*needed} calories')
                        else:
                            print("you reach your calories goal for today!")
                        return
            if id == 0 :
                print("you don't enter your data yet to calculate your progress")
                enter_data = input("want to enter your data? (y/n) ").strip().lower()
                if enter_data == "y":
                    Calories.add_data(self)
                else:
                    return

    def add_calorie(self):
        while True:
            try:
                today=str(datetime.now().date())
                today_calorie=int(input("enter calories you have today"))
                if today_calorie < 0 :
                    print("input must be positive!")
                    redo = input("want to try again? (y/n)").strip().lower()
                    if redo == "y":
                        continue
                    else:
                        return
                found=0
                for user in self.daily_calories:
                    if user.get("user_id") == self.user_id and user.get("date") == today:
                        new_calories = user.get("calories") + today_calorie
                        user["calories"] = new_calories
                        with open("users_calories.json", "w") as file:
                            json.dump(self.daily_calories, file, indent=4)
                        found=1
                if found==0:
                    new_calories=today_calorie
                    user={
                        "user_id":self.user_id,
                        "date":today,
                        "calories":new_calories
                    }
                    self.daily_calories.append(user)
                    with open("users_calories.json", "w") as file:
                        json.dump(self.daily_calories, file, indent=4)
                show_progress=input("want to show your progress? (y/n) ").strip().lower()
                if show_progress =="y":
                    Calories.progress(self)
                return
            except:
                print("invalid input!")
                redo = input("want to try again? (y/n)").strip().lower()
                if redo == "y":
                    continue
                else:
                    return

    def edit_data(self):
        while True:
            try:
                found=0
                for user in self.content:
                    if user.get("user_id")==self.user_id:
                        found=1
                        edit=input("what you want to edit?\n( gender / age / height / weight / goal / TDEE )\n").strip().lower()
                        if edit == "gender":
                            gender = input("what's your gender? (male/female) ").strip().lower()
                            if gender not in ["male", "female"]:
                                print("invalid input!")
                                redo = input("want to try again? (y/n) ").strip().lower()
                                if redo == "y":
                                    continue
                                else:
                                    return
                            user["gender"] = gender
                        elif edit == "age":
                            age = int(input("what's your age?"))
                            if age < 18:
                                print("you must be +18")
                                redo = input("want to try again? (y/n) ").strip().lower()
                                if redo == "y":
                                    continue
                                else:
                                    return
                            user["age"]=age
                        elif edit == "height":
                            height = int(input("what's your height? (in cm) "))
                            if height < 50:
                                print("height must be in cm")
                                redo = input("want to try again? (y/n) ").strip().lower()
                                if redo == "y":
                                    continue
                                else:
                                    return
                            user["height"]=height
                        elif edit == "weight":
                            weight = int(input("what's your weight? (in kg) "))
                            if weight <= 0:
                                print("invalid input!")
                                redo = input("want to try again? (y/n) ").strip().lower()
                                if redo == "y":
                                    continue
                                else:
                                    break
                            user["weight"]=weight
                        elif edit == "goal":
                            goal = input("what's your weight goal? ( maintain / lose / gain )").strip().lower()
                            if goal not in ["maintain", "lose", "gain"]:
                                print("invalid input!")
                                redo = input("want to try again? (y/n) ").strip().lower()
                                if redo == "y":
                                    continue
                                else:
                                    return
                            user["goal"]=goal
                        elif edit == "tdee":
                            tdee=int(input("enter TDEE: "))
                            if tdee <=0:
                                print("invalid input")
                                redo = input("want to try again? (y/n) ").strip().lower()
                                if redo == "y":
                                    continue
                                else:
                                    return
                            user["TDEE"] = tdee
                        else:
                            print("invalid input")
                            redo = input("want to try again? (y/n) ").strip().lower()
                            if redo == "y":
                                continue
                            else:
                                return
                        again=input("want to do another edit? (y/n) ").strip().lower()
                        if again == "y":
                            continue
                        with open("calories.json", "w") as file:
                            json.dump(self.content, file, indent=4)
                        if edit in ['gender','age','height','weight']:
                            Calories.calculate_calories(self)
                        return
                if found == 0:
                    print("you don't enter your data yet")
                    enter_data = input("want to enter your data? (y/n) ").strip().lower()
                    if enter_data == "y":
                        Calories.add_data(self)
                    else:
                        return
            except:
                print("invalid inputs!")
                redo = input("want to try again? (y/n) ").strip().lower()
                if redo == "y":
                    continue
                else:
                    break

    def get_data(self):
        today = str(datetime.now().date())
        found1=0
        found2=0
        for user in self.content:
            if user.get("user_id")==self.user_id:
                found1=1
                print(f'gender: {user.get("gender")}')
                print(f'age: {user.get("age")}')
                print(f'height: {user.get("height")}')
                print(f'weight: {user.get("weight")}')
                print(f'goal: {user.get("goal")}')
                print(f'TDEE: {user.get("TDEE")}')
        for user in self.daily_calories:
            if user.get("user_id")==self.user_id and user.get("date") == today:
                found2=1
                print(f'calories you get for today: {user.get("calories")}')
        if found1 == 0:
            print("you don't enter your data yet")
            enter_data = input("want to enter your data? (y/n) ").strip().lower()
            if enter_data == "y":
                Calories.add_data(self)
        if found2==0:
            print("you don't enter your calories for today yet")
            enter_data = input("want to add calories? (y/n) ").strip().lower()
            if enter_data == "y":
                Calories.add_calorie(self)
        edit=input("want to edit your data? (y/n) ").strip().lower()
        if edit =="y":
            Calories.edit_data(self)

    def suggestions(self):
        while True:
            found=0
            for user in self.content:
                if user.get("user_id")==self.user_id:
                    found=1
                    goal=user.get("goal")
                    with open("meals.json") as file:
                        suggestions=json.load(file)
            if found == 1:
                meals=suggestions.get(goal)
                user_need=input("what meal you want suggestion for?\n( breakfast / lunch / dinner / snacks / all )\n").strip().lower()
                if user_need not in ["breakfast","lunch","dinner","snacks","all"]:
                    print("invalid input!")
                    redo=input("want to try again? (y/n)").strip().lower()
                    if redo == "y" :
                        continue
                    else:
                        break
                elif user_need == "all":
                    print(f'breakfast: {random.choice(meals.get("breakfast"))}')
                    print(f'lunch: {random.choice(meals.get("lunch"))}')
                    print(f'dinner: {random.choice(meals.get("dinner"))}')
                    print(f'snacks: {random.choice(meals.get("snacks"))}')
                else:
                    print(f'{user_need}: {random.choice(meals.get(user_need))}')
                again=input("want another suggestion? (y/n)").strip().lower()
                if again=="y":
                    continue
                else:
                    break
            else:
                print("you don't enter your data yet")
                enter_data = input("want to enter your data? (y/n) ").strip().lower()
                if enter_data == "y":
                    Calories.add_data(self)
                else:
                    return


# while True:
#     person = Calories(user_id)
#     print(f'{"="*10} {"calories list"} {"="*10}')
#     option=input("1.add your data\n2.get your BMI\n3.get your TDEE (calories you need)\n4.add calories you have today\n5.show your progress in your daily need of calories\n6.edit on your data\n7.show your data\n8.suggestions to your meals\n9.back\n")
#     if option == "1":
#         person.add_data()
#     elif option =="2":
#         person.calculate_bmi()
#     elif option == "3":
#         person.calculate_calories()
#     elif option == "4":
#         person.add_calorie()
#     elif option == "5":
#         person.progress()
#     elif option == "6":
#         person.edit_data()
#     elif option == "7":
#         person.get_data()
#     elif option == "8":
#         person.suggestions()
#     elif option == "9":
#         break
#     else:
#         print("invalid input!\nplease try again")
#     enter=input("press to continue...")
