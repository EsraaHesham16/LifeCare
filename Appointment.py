from datetime import datetime


class Appointment:

    def __init__(self, appointment_id, user_id, title, doctor,
                 clinic, date, time, notes, status="Upcoming"):

        self.__appointment_id = appointment_id
        self.__user_id = user_id
        self.title = title
        self.doctor = doctor
        self.clinic = clinic
        self.date = date
        self.time = time
        self.notes = notes
        self.status = status

    @property
    def appointment_id(self):
        return self.__appointment_id

    @property
    def user_id(self):
        return self.__user_id

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        if value.strip() == "":
            raise ValueError("Title of the Appoinment cannot be empty")
        else:
            self.__title = value

    @property
    def doctor(self):
        return self.__doctor

    @doctor.setter
    def doctor(self, value):
        if value.strip() == "":
            raise ValueError("Doctor name cannot be empty")
        else:
            self.__doctor = value

    @property
    def clinic(self):
        return self.__clinic

    @clinic.setter
    def clinic(self, value):
        if value.strip() == "":
            raise ValueError("clinic name cannot be empty")
        else:
            self.__clinic = value

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, value):    
        self.__date = value

    @property
    def time(self):
        return self.__time

    @time.setter
    def time(self, value):
        self.__time = value

    @property
    def notes(self):
        return self.__notes

    @notes.setter
    def notes(self, value):
        self.__notes = value.strip()

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        valid_status = ["Upcoming", "Completed", "Missed", "Cancelled"]

        if value not in valid_status:
            raise ValueError("Invalid status.")
        self.__status = value

    def display_info(self):
        print(f"Appointment ID : {self.__appointment_id}")
        print(f"Title : {self.__title}")
        print(f"Doctor : {self.__doctor}")
        print(f"Clinic : {self.__clinic}")
        print(f"Date : {self.__date}")
        print(f"Time : {self.__time}")
        print(f"status: {self.__status}")
        print(f"Notes : {self.__notes}")

    def to_dict(self):
        return {
            "appointment_id": self.__appointment_id,
            "user_id": self.__user_id,
            "title": self.__title,
            "doctor": self.__doctor,
            "clinic": self.__clinic,
            "date": self.__date.strftime("%Y-%m-%d"),
            "time": self.__time.strftime("%H:%M"),
            "notes": self.__notes,
            "status": self.__status
        }

    # ---------- String Representation ----------

    # __str__() → لعرض ملخص سريع. بايثون بتستدعيها تلقائي عند كتابة (print(medicine)) مثلا
    def __str__(self):
        return f"{self.__title} with Dr. {self.__doctor}"
