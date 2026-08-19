import json
from datetime import datetime,date
class To_Do():
    def __init__(self,user_id):
        self.__user_id=user_id
    def load_todos(self):
        with open("todo.json","r") as file:
            data=json.load(file)
        return data
    def add_task(self):
        title_input=input("Enter the Title")
        while not self.validate_title(title_input):
            print("Title cannot be empty.")
            title_input= input("Enter the Title")
            continue
        description=input("enter the description:")
        time_input= input("Enter the Time:")
        while not self.validate_time(time_input):
            time_input= input("Enter the Time")
            continue
        date_input=input("please enter the date:")
        while not self.validate_date(date_input):
            date_input= input("please enter the date:")
            continue
        data=self.load_todos()
        tasks=data.setdefault(self.__user_id,[])
        #print(tasks)
        tasks.append({
            "title":title_input,
            "description":description,
            "date":date_input,
            "time":time_input,
            "status":"pending"
        })
        data[self.__user_id]=tasks
        with open("todo.json","w") as file:
            json.dump(data,file,indent=2)
    def validate_title(self,title_input):
        title=title_input.strip()
        if title:
            if not title.isdigit():
                return True
            else:
                return False
        else:
            return False
    def validate_time(self,time_input):
        try:
            time=datetime.strptime(time_input,"%H:%M").time()
            return True
        except ValueError:
            print("Invalid time, enter the time as %H:%M.")
            return False
    def validate_date(self,date_input):
        try:
            date_l=datetime.strptime(date_input,"%Y-%m-%d").date()
        except ValueError:
            print("Invalid date, enter the date as %Y-%m-%d.")
            return False
        if date_l>=date.today():
            return True
        else:
            print("Invalid date.Please enter a future date.")
            return False
    def view_tasks(self):
        data=self.load_todos()
        print(f"{"="*20}VIEW TASKS{"="*20}")
        while True:
            print(f"1-today's Tasks\n2-All Tasks\n3-Pending Tasks\n4-Completed Tasks\n5-Overdue Tasks\n6-Back")
            user_choice=input("Enter your choice:")
            #print(user_choice)
            if user_choice=="1":
                #print(data[self.__user_id])
                print(f"{"="*30}\n{"TODAY'S TASKS":>21}\n{"="*30}")
                today_tasks=self.today_tasks()
                count=0
                for task in today_tasks:
                    count+=1
                    print(f"{count}-{task["title"]}\n  {task["description"]}\n  {task["time"]}\n  {task["status"]}")
                if count==0:
                    print("No tasks scheduled for today.Enjoy your day!")
                else:
                    print(f"{"_"*30}\nYou have {count} tasks scheduled for today.\n")
            elif user_choice=="2":
                print(f"{"=" * 30}\n{"ALL TASKS":>19}\n{"=" * 30}")
                count=0
                for task in data[self.__user_id]:
                    count += 1
                    print(f"{count}-{task["title"]}\n  {task["description"]}\n  {task["time"]}\n  {task["status"]}\n")
                if count== 0:
                    print("you don't have any tasks yet.start by adding your first task!!")
                else:
                    print(f"{"_" * 30}\nYou have {count} tasks in total.\n")
            elif user_choice=="3":
                print(f"{"=" * 30}\n{"PENDING TASKS":>21}\n{"=" * 30}")
                pending_list=self.pending_tasks()
                count=0
                for task in pending_list:
                    count+=1
                    print(f"{count}-{task["title"]}\n  {task["description"]}\n  {task["time"]}\n  {task["status"]}\n")
                if count == 0:
                    print("Great job!you don't have any pending tasks !")
                else:
                    print(f"{"-" * 30}\nYou have {count} pending tasks.keep going! ")
            elif user_choice=="4":
                print(f"{"=" * 30}\n{"COMPLETED TASKS":>21}\n{"=" * 30}")
                data = self.load_todos()
                completed_list=[]
                for task in data[self.__user_id]:
                    if task["status"] == "completed":
                        completed_list.append(task)
                count = 0
                for task in completed_list:
                    count += 1
                    print(f"{count}-{task["title"]}\n  {task["description"]}\n  {task["time"]}\n  {task["status"]}\n")
                if count== 0:
                    print("No completed tasks yet.keep going,you've got this!")
                else:
                    print(f"{"-" * 30}\nYou have completed {count} tasks.Great job!")
            elif user_choice=="5":
                overdue_list=self.overdue_tasks()
                count=0
                for task in overdue_list:
                    count+=1
                    print(f"{count}-{task["title"]}\n  {task["description"]}\n  {task["time"]}\n  {task["status"]}\n")
                if count== 0:
                    print("you don't have any overdue tasks.")
                else:
                    print(f"{"-" * 30}\nYou missed {count} task deadlines.these tasks are still pending!")
            else:
                if user_choice=="6":
                    return False
    def pending_tasks(self):
        data=self.load_todos()
        pending_list=[]
        for task in data[self.__user_id]:
            if task["status"]=="pending":
                pending_list.append(task)
        return pending_list
    def overdue_tasks(self):
        data=self.load_todos()
        overdue_list = []
        for task in data[self.__user_id]:
            task_date= datetime.strptime(task["date"], "%Y-%m-%d").date()
            if task_date<date.today():
                overdue_list.append(task)
        return overdue_list
    def today_tasks(self):
        data=self.load_todos()
        today_tasks_l=[]
        for task in data[self.__user_id]:
            task_date = datetime.strptime(task["date"], "%Y-%m-%d").date()
            if task_date == date.today():
                today_tasks_l.append(task)
        return today_tasks_l
    def mark_completed(self):
        data=self.load_todos()
        print(f"{"=" * 30}\n{"PENDING TASKS":>21}\n{"=" * 30}")
        while True:
            tasks = self.pending_tasks()
            count=0
            for task in tasks:
                count+=1
                print(f"{count}-{task["title"]}\n  {task["description"]}\n  {task["date"]}  {task["time"]}\n  {task["status"]}\n")
            if count==0:
                print("you don't have any pending tasks to mark as completed")
                break
            try:
                choice=int(input(f"Which task would you like to mark as complete?\nEnter the task number:"))
            except ValueError:
                print("Invalid input.Please enter a task number.")
                continue
            if choice>count or choice<1:
                print(f"\nInvalid task number.please choose a task from the list \n")
                continue
            selected_task=tasks[choice-1]
            for task in data[self.__user_id]:
                if task==selected_task:
                    task["status"]="completed"
                    break
            with open("todo.json","w") as file:
                json.dump(data,file,indent=2)
            print(f"{"["}{selected_task["title"]}{"]"} has been marked as completed successfully!\n ")
            choice2= input("would you like to mark another task as completed?(y/n):")
            if choice2 == "y":
                continue
            else:
                break
    def delete_task(self):
        data=self.load_todos()
        tasks = data[self.__user_id]
        while True:
            print(f"{"=" * 30}\n{"ALL TASKS":>19}\n{"=" * 30}")
            count = 0
            for task in tasks:
                count+= 1
                print(f"{count}-{task["title"]}\n  {task["description"]}\n  {task["date"]}  {task["time"]}\n  {task["status"]}\n")
            if count==0:
                print("you don't have any tasks to delete ")
                break
            try:
                choice=int(input("Enter the task number you want to delete:"))
            except ValueError:
                print("Invalid input.Please enter a task number.")
                continue
            if choice>count or choice<1:
                print("Invalid task number.please choose a task from the list")
                continue
            user_choice=input(f"Are you sure you want to delete {tasks[choice-1]["title"]}?(y/n):")
            if user_choice=="y":
                del tasks[choice-1]
                data[self.__user_id]=tasks
                with open("todo.json","w") as file:
                    json.dump(data,file,indent=2)
                print("Task deleted successfully!")
                choice2 = input("would you like to delete another task?(y/n):")
                if choice2 == "y":
                    continue
                else:
                    break
            else:
                print("Task deletion cancelled.")
                choice2=input("would you like to delete another task?(y/n):")
                if choice2=="y":
                    continue
                else:
                    break
    def edit_task(self):
        data=self.load_todos()
        while True:
            print(f"{"=" * 30}\n{"EDIT TASK":>19}\n{"=" * 30}")
            count = 0
            for task in data[self.__user_id]:
                count += 1
                print(f"{count}-{task["title"]}\n  {task["description"]}\n  {task["date"]}  {task["time"]}\n  {task["status"]}\n")
            if count == 0:
                print("you don't have any tasks to edit.")
                break
            try:
                choice=int(input("Enter the task number you want to edit:"))
            except ValueError:
                print("Invalid input.Please enter a task number.")
                continue
            if choice>count or choice<1:
                print("Invalid task number.please choose a task from the list")
                continue
            selected_task=data[self.__user_id][choice-1]
            print(f"{"=" * 30}\n{"SELECTED TASK":>19}\n{"=" * 30}")
            print(f" {selected_task["title"]}\n {selected_task["description"]}\n {selected_task["date"]}  {selected_task["time"]}\n {selected_task["status"]}\n\n")
            print(f"What would you like to edit?\n\n1.Tilte\n2.Description\n3.Date\n4.Time\n5.Back")
            user_choice=input("Choose an option:")
            if user_choice=="1":
                new_title= input("Enter the new Title")
                while not self.validate_title(new_title):
                    print("Title cannot be empty.")
                    new_title= input("Enter the new Title")
                    continue
                data[self.__user_id][choice - 1]["title"]=new_title
                with open("todo.json","w") as file:
                    json.dump(data,file,indent=2)
                    print("Task Update successfully!")
                    continue
            elif user_choice=="2":
                new_description= input("Enter the new description:")
                data[self.__user_id][choice - 1]["description"]=new_description
                with open("todo.json","w") as file:
                    json.dump(data,file,indent=2)
                    print("Task Update successfully!")
                    continue
            elif user_choice=="3":
                new_date= input("Enter the new Date:")
                while not self.validate_date(new_date):
                    new_date= input("please enter the new date:")
                    continue
                data[self.__user_id][choice - 1]["date"] = new_date
                with open("todo.json", "w") as file:
                    json.dump(data, file, indent=2)
                    print("Task Update successfully!")
                    continue
            elif user_choice=="4":
                new_time= input("Enter the new time:")
                while not self.validate_time(new_time):
                    new_time= input("Enter the new Time")
                    continue
                data[self.__user_id][choice - 1]["time"] = new_time
                with open("todo.json", "w") as file:
                    json.dump(data, file, indent=2)
                    print("Task Update successfully!")
                    continue
            elif user_choice=="5":
                break
            else:
                print("Invalid task number.Please choose a task from the list.")
                continue

user1=To_Do("33")

