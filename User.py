import json
class User():
    def __init__(self):
        self.__name=None
        self.__email=None
        self.__password=None
        self.__user_id=None
    def set_name(self,name):
        if len(name) >3 and name.replace(" ","").isalpha():
            self.__name=name
            return True
        else:
            print("Invalid name")
            return False
    def set_email(self,email):
        data_users=self.load_users()
        invalid_email=False
        if (len(email)< 3) or "@" not in email or "." not in email:
            invalid_email=True
            print("Invalid email")
        found=False
        for key, value in data_users.items():
            if email == value["email"]:
                print("This email already exists,please enter another one")
                found = True
        if invalid_email or found:
            return False
        else:
            self.__email = email
            return True
    def set_password(self,password):
        if len(password.strip())>=8 and " " not in password:
            self.__password=password
            return True
        else:
            return False
    def load_users(self):
        with open("users.json","r") as file:
            data=json.load(file)
            return data
    def register(self):
        data_users=self.load_users()
        print(f"{"="*30}\n {"Register":>18}\n{"="*30}")
        while True:
            name = input("Name:")
            if self.set_name(name):
                break
            else:
                print("Try again")
        while True:
            email = input("Email:")
            if self.set_email(email):
               break
            else:
               print("Try again")

        while True:
            password = input("Password:")
            if self.set_password(password):
                break
            else:
                print("Invalid password,please try again")
        max_id=0
        for user_id in data_users:
            if int(user_id)>max_id:
                max_id=int(user_id)
        self.__user_id=str(max_id+1)
        data_users[self.__user_id]={
            "name":self.__name,
            "email":self.__email,
            "password":self.__password
            }
        print("Your account has been created successfully.")
        with open("users.json","w") as file:
            json.dump(data_users,file,indent=4)
            return str(self.__user_id)
    def show_profile(self):
        print(f"{"="*20}Your Profile{"="*20}")
        print(f"Name:{self.__name}\nEmail:{self.__email}\nPassword:{"*"*len(self.__password)}")
    def edit_profile(self):
        while True:
            print(f"\nName:{self.__name}\nEmail:{self.__email}\n")
            user_choice=input("What do you want to edit?\n\n1.Edit Name\n2.Edit Email\n3.Edit Password\n4.Back\n\nEnter your choice:")
            if user_choice=="1" or user_choice=="edit name":
                 while True:
                     new_name = input("Enter your new name:")
                     if self.set_name(new_name):
                         print("Name updated successfully")
                         data_users = self.load_users()
                         data_users[self.__user_id] = {
                             "name": self.__name,
                             "email": self.__email,
                             "password": self.__password
                         }
                         with open("users.json", "w") as file:
                             json.dump(data_users, file, indent=2)
                         break
                     else:
                         print("Try again")
            elif user_choice=="2" or user_choice=="edit email":
                 while True:
                     new_email= input("Enter your new email:")
                     if self.set_email(new_email):
                         self.__email=new_email
                         print("Email updated successfully")
                         data_users = self.load_users()
                         data_users[self.__user_id] = {
                             "name": self.__name,
                             "email": self.__email,
                             "password": self.__password
                         }
                         with open("users.json", "w") as file:
                             json.dump(data_users, file, indent=2)
                         break
                     else:
                         print("Try again")
            elif user_choice=="3" or user_choice=="edit password":
                 old_password=input("Enter your current password:")
                 if old_password==self.__password:
                     while True:
                         new_password = input("Enter your new password:")
                         if self.set_password(new_password):
                             print("Password changed successfully")
                             data_users = self.load_users()
                             data_users[self.__user_id] = {
                                 "name": self.__name,
                                 "email": self.__email,
                                 "password": self.__password
                             }
                             with open("users.json", "w") as file:
                                 json.dump(data_users, file, indent=2)
                             break
                         else:
                             print("Invalid Password\nTry again")
                 else:
                     print("Wrong password")
            else:
                break
    def login(self):
        data_users=self.load_users()
        email = input("Email:")
        password = input("Password:")
        found=False
        for key, value in data_users.items():
            if value["email"] == email and value["password"] == password:
                print(f"Login successful.\nWelcome {value["name"]}!")
                found=True
                self.__user_id=key
                self.__name = value["name"]
                self.__email = value["email"]
                self.__password=value["password"]
                return key
        if not found:
            print("Wrong email or password!")
            return False
    def delete_account(self):
        data_users=self.load_users()
        while True:
            email = input("Enter your email:")
            password = input("Enter your password:")
            if email ==self.__email and password == self.__password:
                user = input("Are you sure you want to delete your account?(yes/no):")
                print(type(self.__user_id))
                if user == "yes":
                    data_users.pop(str(self.__user_id))
                    with open("users.json", "w") as file:
                        json.dump(data_users, file, indent=2)
                        print("Account deleted successfully.")
                        break
            else:
                print("Wrong email or password!")
                continue

# print(f"{"="*20}WELCOME TO LIFE CARE{"="*20}\n")
# print("Let's get started!\n")
# print(f"1.Register\n2.Login\n3.Exit")
# logout=True
# while logout:
#     choice = input("Enter your choice:")
#     user1=User()

#     if choice=="1" or choice=="register":
#         print("\nPlease enter your information")
#         user1.register()
#         while True:
#             print(f"\n1.Show Profile\n2.Edit Profile\n3.Delete Account\n4.Logout")
#             user_choice=input("Enter your choice:")
#             if user_choice=="1" or user_choice=="show Profile":
#                 user1.show_profile()
#                 input(f"\nPress Enter to continue..")
#                 continue
#             elif user_choice=="2" or user_choice=="edit Profile":
#                 user1.edit_profile()
#                 input(f"\nPress Enter to continue..")
#                 continue
#             elif user_choice=="3" or user_choice=="delete Account":
#                 user1.delete_account()
#                 input(f"\n Press Enter to continue..")
#                 logout= False
#                 break
#             else:
#                 if user_choice=="4" or user_choice=="logout":
#                     logout=False
#                     break

#     if choice=="2" or choice=="login":
#         user1.login()
#         while True:
#             print(f"1.Show Profile\n2.Edit Profile\n3.Delete Account\n4.Logout")
#             user_choice=input("Enter your choice:")
#             if user_choice=="1" or user_choice=="show Profile":
#                 user1.show_profile()
#                 input(f"\n Press Enter to continue..")
#                 continue
#             elif user_choice=="2" or user_choice=="edit Profile":
#                 user1.edit_profile()
#                 input(f"\n Press Enter to continue..")
#                 continue
#             elif user_choice=="3" or user_choice=="delete Account":
#                 user1.delete_account()
#                 input(f"\n Press Enter to continue..")
#                 logout = False
#                 break
#             else:
#                 if user_choice=="4" or user_choice=="logout":
#                     logout = False
#                     break
#     else:
#         if choice=="3" or choice=="back":
#             print("Goodbye!")
#             break
