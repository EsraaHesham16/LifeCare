from datetime import datetime


class Medicine:

    def __init__(self, medicine_id, user_id, medicine_name, dose,
                 times_per_day, times, start_date, end_date, taken=None, completion_notified=False,
                 reminder_notified=False):

        self.__medicine_id = medicine_id
        self.__user_id = user_id
        self.medicine_name = medicine_name
        self.dose = dose
        self.times_per_day = times_per_day
        self.times = times
        self.start_date = start_date
        self.end_date = end_date
        if taken is None:
            self.__taken = {}
        else:
            self.__taken = taken
        self.completion_notified = completion_notified
        self.reminder_notified = reminder_notified

    @property
    def medicine_id(self):
        return self.__medicine_id

    @property
    def user_id(self):
        return self.__user_id

    @property
    def medicine_name(self):
        return self.__medicine_name

    @medicine_name.setter
    def medicine_name(self, value):
        if value.strip() == "":
            raise ValueError("Medicine name cannot be empty")
        else:
            self.__medicine_name = value

    @property
    def dose(self):
        return self.__dose

    @dose.setter
    def dose(self, value):
        if value.strip() == "":
            raise ValueError("Medicine Dose cannot be empty")
        else:
            self.__dose = value

    @property
    def times_per_day(self):
        return self.__times_per_day

    @times_per_day.setter
    def times_per_day(self, value):
        if value > 0 and value <= 6:
            self.__times_per_day = value
        else:
            raise ValueError("Number of doses must be greater than zero and less than 6.")

    @property
    def times(self):
        return self.__times

    @times.setter
    def times(self, value):
        if len(value) == self.__times_per_day:
            self.__times = value
        else:
            raise ValueError(
                f"You entered {self.__times_per_day} doses per day, so you must enter {self.__times_per_day} times.")

    @property
    def start_date(self):
        return self.__start_date

    @start_date.setter
    def start_date(self, value):
       self.__start_date = value
       
    @property
    def end_date(self):
        return self.__end_date

    @end_date.setter
    def end_date(self, value):
        if value >= self.__start_date:
            self.__end_date = value
        else:
            raise ValueError("End Date MUST be After Start Date!")

    @property
    def reminder_notified(self):
        return self.__reminder_notified

    @reminder_notified.setter
    def reminder_notified(self, value):
        self.__reminder_notified = value

    @property
    def completion_notified(self):
        return self.__completion_notified

    @completion_notified.setter
    def completion_notified(self, value):
        self.__completion_notified = value

    @property
    def taken(self):
        return self.__taken

    def display_info(self):
        print(f"Medicine ID : {self.__medicine_id}")
        print(f"Medicine Name : {self.__medicine_name}")
        print(f"Dose : {self.__dose}")
        print(f"Times Per Day : {self.__times_per_day}")
        print(f"Times : {', '.join(t.strftime('%H:%M') for t in self.__times)}")
        print(f"Start Date : {self.__start_date}")
        print(f"End Date : {self.__end_date}")

    def to_dict(self):
        return {
            "medicine_id": self.__medicine_id,
            "user_id": self.__user_id,
            "medicine_name": self.__medicine_name,
            "dose": self.__dose,
            "times_per_day": self.__times_per_day,
            "times": [t.strftime("%H:%M") for t in self.__times],
            "start_date": self.__start_date.strftime("%Y-%m-%d"),
            "end_date": self.__end_date.strftime("%Y-%m-%d"),
            "taken": self.__taken,
            "completion_notified": self.__completion_notified,
            "reminder_notified": self.__reminder_notified
        }

    # ---------- String Representation ----------

    # __str__() → لعرض ملخص سريع. بايثون بتستدعيها تلقائي عند كتابة (print(medicine)) مثلا
    def __str__(self):
        return f"{self.__medicine_name} ({self.__dose})"


