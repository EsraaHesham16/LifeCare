import json
import os
import sys
from datetime import datetime, date, timedelta
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Import existing domain modules
from User import User
from water import WaterTracker, load_water, save_water
from sleep import SleepTracker, load_sleep, save_sleep
from activity_tracker import ActivityTracker
from mood_tracker import MoodTracker
from MedicineProcesses import MedicineProcesses
from medicine import Medicine
from Appointmentmanager import AppointmentManager
from Appointment import Appointment
from dashboard import DashBoard
from report import Reports

PORT = 5000
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd(), 'static')

def get_users_dict():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_users_dict(data):
    with open("users.json", "w") as f:
        json.dump(data, f, indent=4)

class HealthAppHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        sys.stdout.write(f"[{self.log_date_time_string()}] {format % args}\n")
        sys.stdout.flush()

    def send_json(self, data, code=200):
        body = json.dumps(data).encode('utf-8')
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def get_body(self):
        content_len = int(self.headers.get('Content-Length', 0))
        if content_len > 0:
            post_body = self.rfile.read(content_len)
            try:
                return json.loads(post_body.decode('utf-8'))
            except Exception:
                return {}
        return {}

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        # Route API calls
        if path.startswith('/api/'):
            return self.handle_api_get(path, query)

        # Serve static files
        if path == '/':
            filepath = os.path.join(STATIC_DIR, 'index.html')
        else:
            rel_path = path.lstrip('/')
            filepath = os.path.join(STATIC_DIR, rel_path)

        if os.path.isfile(filepath):
            self.send_response(200)
            if filepath.endswith('.html'): self.send_header('Content-Type', 'text/html')
            elif filepath.endswith('.css'): self.send_header('Content-Type', 'text/css')
            elif filepath.endswith('.js'): self.send_header('Content-Type', 'application/javascript')
            elif filepath.endswith('.png'): self.send_header('Content-Type', 'image/png')
            elif filepath.endswith('.json'): self.send_header('Content-Type', 'application/json')
            self.end_headers()
            with open(filepath, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404, "File Not Found")

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        body = self.get_body()

        if path == '/api/auth/login':
            email = body.get('email', '').strip()
            password = body.get('password', '').strip()
            users = get_users_dict()
            for uid, user_data in users.items():
                if user_data.get('email') == email and user_data.get('password') == password:
                    return self.send_json({"success": True, "user": {"user_id": str(uid), "name": user_data.get("name"), "email": user_data.get("email")}})
            return self.send_json({"success": False, "message": "Invalid email or password"}, 401)

        elif path == '/api/auth/register':
            name = body.get('name', '').strip()
            email = body.get('email', '').strip()
            password = body.get('password', '').strip()

            if len(name) <= 3 or not name.replace(" ", "").isalpha():
                return self.send_json({"success": False, "message": "Name must be > 3 letters"}, 400)
            if len(email) < 3 or "@" not in email or "." not in email:
                return self.send_json({"success": False, "message": "Invalid email format"}, 400)
            
            users = get_users_dict()
            for uid, val in users.items():
                if val.get("email") == email:
                    return self.send_json({"success": False, "message": "Email already exists"}, 400)

            if len(password) < 8 or " " in password:
                return self.send_json({"success": False, "message": "Password must be >= 8 chars with no spaces"}, 400)

            max_id = 0
            for uid in users:
                try:
                    if int(uid) > max_id: max_id = int(uid)
                except ValueError: pass

            new_id = str(max_id + 1)
            users[new_id] = {"name": name, "email": email, "password": password}
            save_users_dict(users)
            return self.send_json({"success": True, "user": {"user_id": new_id, "name": name, "email": email}})

        elif path.startswith('/api/water/') and path.endswith('/add'):
            uid = path.split('/')[3]
            wt = WaterTracker(str(uid))
            wt.add_cup()
            today_data = wt.get_today_water()
            return self.send_json({
                "success": True,
                "today": {
                    "cups": today_data["cups"],
                    "goal": today_data["goal"],
                    "progress": wt.get_water_progress(),
                    "streak": wt.calculate_water_streak()
                }
            })

        elif path.startswith('/api/sleep/') and path.endswith('/add'):
            uid = path.split('/')[3]
            sleep_time = body.get('sleep_time', '').strip()
            wake_time = body.get('wake_time', '').strip()
            quality = body.get('quality', 'Good')

            if not sleep_time or not wake_time or sleep_time == wake_time:
                return self.send_json({"success": False, "message": "Invalid sleep/wake time"}, 400)

            try:
                sleep_dt = datetime.strptime(sleep_time, "%H:%M")
                wake_dt = datetime.strptime(wake_time, "%H:%M")
            except ValueError:
                return self.send_json({"success": False, "message": "Use HH:MM format"}, 400)

            if wake_dt < sleep_dt: wake_dt += timedelta(days=1)
            duration_hrs = round((wake_dt - sleep_dt).total_seconds() / 3600, 2)

            st = SleepTracker(str(uid))
            today_str = str(date.today())
            existing = False
            for rec in st.data:
                if str(rec.get("user_id")) == str(uid) and rec.get("date") == today_str:
                    rec["hours"] = duration_hrs
                    rec["quality"] = quality
                    existing = True
                    break
            if not existing:
                st.data.append({"user_id": str(uid), "date": today_str, "hours": duration_hrs, "quality": quality, "goal": 8})
            save_sleep(st.data)
            return self.send_json({"success": True, "streak": st.calculate_sleep_streak()})

        elif path.startswith('/api/activity/') and path.endswith('/add'):
            uid = path.split('/')[3]
            steps = int(body.get('steps', 0))
            duration = int(body.get('duration', 0))
            at = ActivityTracker(str(uid))
            today_str = str(date.today())

            for item in at.content:
                if str(item.get("user_id")) == str(uid) and item.get("date") == today_str:
                    item["steps"] = steps
                    item["duration"] = duration
                    with open("activity.json", "w") as f: json.dump(at.content, f, indent=4)
                    return self.send_json({"success": True, "record": item})

            new_rec = {"user_id": str(uid), "date": today_str, "steps": steps, "duration": duration}
            at.content.append(new_rec)
            with open("activity.json", "w") as f: json.dump(at.content, f, indent=4)
            return self.send_json({"success": True, "record": new_rec})

        elif path.startswith('/api/mood/') and path.endswith('/add'):
            uid = path.split('/')[3]
            user_mood = body.get('mood', '').strip().lower()
            mt = MoodTracker(str(uid))
            today_str = str(date.today())
            for item in mt.content:
                if str(item.get("user_id")) == str(uid) and item.get("date") == today_str:
                    item["mood"] = user_mood
                    with open("mood.json", "w") as f: json.dump(mt.content, f, indent=4)
                    return self.send_json({"success": True, "record": item})

            new_rec = {"user_id": str(uid), "date": today_str, "mood": user_mood}
            mt.content.append(new_rec)
            with open("mood.json", "w") as f: json.dump(mt.content, f, indent=4)
            return self.send_json({"success": True, "record": new_rec})

        elif path.startswith('/api/medicines/') and path.endswith('/add'):
            uid = path.split('/')[3]
            name = body.get('medicine_name', '').strip()
            dose = body.get('dose', '').strip()
            times_per_day = int(body.get('times_per_day', 1))
            times = body.get('times', [])
            start_date_str = body.get('start_date', str(date.today()))
            end_date_str = body.get('end_date', str(date.today()))

            try:
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            except ValueError:
                return self.send_json({"success": False, "message": "Invalid date format"}, 400)

            mp = MedicineProcesses()
            max_id = 0
            for item in mp._MedicineProcesses__medicine_list:
                try:
                    if int(item.medicine_id) > max_id: max_id = int(item.medicine_id)
                except (ValueError, TypeError): pass

            time_objs = [datetime.strptime(t, "%H:%M").time() for t in times]
            new_med = Medicine(max_id + 1, str(uid), name, dose, times_per_day, time_objs, start_date, end_date)
            mp._MedicineProcesses__medicine_list.append(new_med)
            mp.save_data()
            return self.send_json({"success": True, "medicine": new_med.to_dict()})

        elif path.startswith('/api/medicines/') and path.endswith('/mark_taken'):
            uid = path.split('/')[3]
            med_id = body.get('medicine_id')
            dose_index = body.get('dose_index', 0)
            mp = MedicineProcesses()
            today_str = str(date.today())

            for med in mp._MedicineProcesses__medicine_list:
                if str(med.user_id) == str(uid) and str(med.medicine_id) == str(med_id):
                    if today_str not in med.taken:
                        med.taken[today_str] = [False] * med.times_per_day
                    if 0 <= dose_index < med.times_per_day:
                        med.taken[today_str][dose_index] = True
                        mp.save_data()
                        return self.send_json({"success": True, "medicine": med.to_dict()})
            return self.send_json({"success": False, "message": "Medicine not found"}, 404)

        elif path.startswith('/api/appointments/') and path.endswith('/add'):
            uid = path.split('/')[3]
            title = body.get('title', '').strip()
            doctor = body.get('doctor', '').strip()
            clinic = body.get('clinic', '').strip()
            date_str = body.get('date', '').strip()
            time_str = body.get('time', '').strip()
            notes = body.get('notes', '').strip()

            try:
                appt_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                appt_time = datetime.strptime(time_str, "%H:%M").time()
            except ValueError:
                return self.send_json({"success": False, "message": "Invalid date or time"}, 400)

            am = AppointmentManager()
            max_id = 0
            for appt in am.get_all_appointmentss():
                try:
                    if int(appt.appointment_id) > max_id: max_id = int(appt.appointment_id)
                except (ValueError, TypeError): pass

            new_id = str(max_id + 1)
            new_appt = Appointment(new_id, str(uid), title, doctor, clinic, appt_date, appt_time, notes)
            am.get_all_appointmentss().append(new_appt)
            am.save_data()
            return self.send_json({"success": True, "appointment": new_appt.to_dict()})

        elif path.startswith('/api/appointments/') and path.endswith('/status'):
            uid = path.split('/')[3]
            appt_id = str(body.get('appointment_id', ''))
            status = body.get('status', '').strip()
            am = AppointmentManager()
            for appt in am.get_all_appointmentss():
                if str(appt.user_id) == str(uid) and str(appt.appointment_id) == appt_id:
                    appt.status = status
                    am.save_data()
                    return self.send_json({"success": True, "appointment": appt.to_dict()})
            return self.send_json({"success": False, "message": "Appointment not found"}, 404)

        self.send_error(404, "Endpoint Not Found")

    def do_PUT(self):
        parsed = urlparse(self.path)
        path = parsed.path
        body = self.get_body()

        if path.startswith('/api/auth/profile/'):
            uid = path.split('/')[4]
            users = get_users_dict()
            str_uid = str(uid)
            if str_uid not in users:
                return self.send_json({"success": False, "message": "User not found"}, 404)

            u = users[str_uid]
            if 'name' in body and body['name']: u['name'] = body['name'].strip()
            if 'email' in body and body['email']: u['email'] = body['email'].strip()
            if 'new_password' in body and body['new_password']:
                if body.get('old_password') != u['password']:
                    return self.send_json({"success": False, "message": "Wrong old password"}, 400)
                u['password'] = body['new_password'].strip()

            users[str_uid] = u
            save_users_dict(users)
            return self.send_json({"success": True, "user": {"user_id": str_uid, "name": u["name"], "email": u["email"]}})

        self.send_error(404)

    def do_DELETE(self):
        parsed = urlparse(self.path)
        path = parsed.path
        parts = path.split('/')

        if path.startswith('/api/medicines/') and len(parts) >= 5 and parts[4] == 'delete':
            uid = parts[3]
            med_id = parts[5]
            mp = MedicineProcesses()
            target = None
            for med in mp._MedicineProcesses__medicine_list:
                if str(med.user_id) == str(uid) and str(med.medicine_id) == str(med_id):
                    target = med
                    break
            if target:
                mp._MedicineProcesses__medicine_list.remove(target)
                mp.save_data()
                return self.send_json({"success": True, "message": "Deleted"})
            return self.send_json({"success": False, "message": "Not found"}, 404)

        elif path.startswith('/api/appointments/') and len(parts) >= 5 and parts[4] == 'delete':
            uid = parts[3]
            appt_id = parts[5]
            am = AppointmentManager()
            target = None
            for appt in am.get_all_appointmentss():
                if str(appt.user_id) == str(uid) and str(appt.appointment_id) == str(appt_id):
                    target = appt
                    break
            if target:
                am.get_all_appointmentss().remove(target)
                am.save_data()
                return self.send_json({"success": True, "message": "Deleted"})
            return self.send_json({"success": False, "message": "Not found"}, 404)

        self.send_error(404)

    def handle_api_get(self, path, query):
        parts = path.split('/')

        if path.startswith('/api/auth/profile/'):
            uid = parts[4]
            users = get_users_dict()
            u = users.get(str(uid))
            if u:
                return self.send_json({"success": True, "user": {"user_id": str(uid), "name": u.get("name"), "email": u.get("email")}})
            return self.send_json({"success": False, "message": "Not found"}, 404)

        elif path.startswith('/api/water/'):
            uid = parts[3]
            wt = WaterTracker(str(uid))
            today_data = wt.get_today_water()
            return self.send_json({
                "success": True,
                "today": {
                    "cups": today_data["cups"],
                    "goal": today_data["goal"],
                    "progress": wt.get_water_progress(),
                    "streak": wt.calculate_water_streak()
                },
                "history": wt.get_water_history()
            })

        elif path.startswith('/api/sleep/'):
            uid = parts[3]
            st = SleepTracker(str(uid))
            today_str = str(date.today())
            today_record = None
            user_history = []
            for rec in st.data:
                if str(rec.get("user_id")) == str(uid):
                    user_history.append(rec)
                    if rec.get("date") == today_str: today_record = rec
            return self.send_json({
                "success": True,
                "today": today_record,
                "streak": st.calculate_sleep_streak(),
                "history": user_history
            })

        elif path.startswith('/api/activity/'):
            uid = parts[3]
            at = ActivityTracker(str(uid))
            today_str = str(date.today())
            today_record = None
            user_history = []
            for item in at.content:
                if str(item.get("user_id")) == str(uid):
                    user_history.append(item)
                    if item.get("date") == today_str: today_record = item

            dates = [item["date"] for item in user_history]
            dates.sort(reverse=True)
            streak = 0
            date1 = date.today()
            if dates:
                if dates[0] == str(date1):
                    dates.pop(0)
                    streak = 1
                for d_str in dates:
                    d_obj = datetime.strptime(d_str, "%Y-%m-%d").date()
                    if (date1 - d_obj).days == 1:
                        streak += 1
                        date1 = d_obj
                    else: break

            return self.send_json({"success": True, "today": today_record, "streak": streak, "history": user_history})

        elif path.startswith('/api/mood/'):
            uid = parts[3]
            mt = MoodTracker(str(uid))
            today_str = str(date.today())
            today_record = None
            user_history = []
            for item in mt.content:
                if str(item.get("user_id")) == str(uid):
                    user_history.append(item)
                    if item.get("date") == today_str: today_record = item

            dates = [item["date"] for item in user_history]
            dates.sort(reverse=True)
            streak = 0
            date1 = date.today()
            if dates:
                if dates[0] == str(date1):
                    dates.pop(0)
                    streak = 1
                for d_str in dates:
                    d_obj = datetime.strptime(d_str, "%Y-%m-%d").date()
                    if (date1 - d_obj).days == 1:
                        streak += 1
                        date1 = d_obj
                    else: break

            return self.send_json({"success": True, "today": today_record, "streak": streak, "history": user_history})

        elif path.startswith('/api/medicines/'):
            uid = parts[3]
            mp = MedicineProcesses()
            user_meds = mp.get_all_medicines(str(uid))
            today = date.today()
            notifications = []
            for med in user_meds:
                if today > med.end_date and not med.completion_notified:
                    notifications.append({"medicine_id": med.medicine_id, "title": f"Completed {med.medicine_name}", "message": "Hope you're feeling much better!"})
                elif (med.end_date - today).days == 1 and not med.reminder_notified:
                    notifications.append({"medicine_id": med.medicine_id, "title": "Finishing Soon", "message": f"{med.medicine_name} finishes tomorrow."})
                elif today == med.end_date:
                    notifications.append({"medicine_id": med.medicine_id, "title": "Last Day", "message": f"Today is last day for {med.medicine_name}."})

            return self.send_json({"success": True, "medicines": [m.to_dict() for m in user_meds], "notifications": notifications})

        elif path.startswith('/api/appointments/'):
            uid = parts[3]
            am = AppointmentManager()
            all_apps = []
            today_apps = []
            today = date.today()
            for appt in am.get_all_appointmentss():
                if str(appt.user_id) == str(uid):
                    dict_rep = appt.to_dict()
                    all_apps.append(dict_rep)
                    if appt.date == today: today_apps.append(dict_rep)
            return self.send_json({"success": True, "appointments": all_apps, "today_appointments": today_apps})

        elif path.startswith('/api/dashboard/'):
            uid = parts[3]
            db = DashBoard()
            return self.send_json({
                "success": True,
                "user": db.get_user(str(uid)),
                "water": db.get_water(str(uid)),
                "sleep": db.get_sleep(str(uid)),
                "activity": db.get_activity(str(uid)),
                "mood": db.get_mood(str(uid)),
                "next_appointment": db.get_appointment(str(uid))
            })

        elif path.startswith('/api/reports/'):
            uid = parts[3]
            rep = Reports()
            report_type = query.get('type', ['daily'])[0].lower()
            str_uid = str(uid)

            with open("water.json", "r") as f: water_data = json.load(f)
            with open("sleep.json", "r") as f: sleep_data = json.load(f)
            with open("activity.json", "r") as f: activity_data = json.load(f)
            with open("mood.json", "r") as f: mood_data = json.load(f)

            today_str = str(date.today())

            if report_type == 'daily':
                water_cups = next((i["cups"] for i in water_data if str(i.get("user_id")) == str_uid and i.get("date") == today_str), 0)
                sleep_hours = next((i["hours"] for i in sleep_data if str(i.get("user_id")) == str_uid and i.get("date") == today_str), 0)
                steps = next((i["steps"] for i in activity_data if str(i.get("user_id")) == str_uid and i.get("date") == today_str), 0)
                mood_val = next((i["mood"] for i in mood_data if str(i.get("user_id")) == str_uid and i.get("date") == today_str), "normal")

                score = rep.calculate_health_score(water_cups, sleep_hours, steps, mood_val)

                badges = []
                if water_cups >= 8: badges.append({"id": "water", "name": "Water Master", "icon": "💧"})
                if sleep_hours >= 8: badges.append({"id": "sleep", "name": "Sleep Hero", "icon": "😴"})
                if steps >= 8000: badges.append({"id": "steps", "name": "Step Champion", "icon": "👟"})
                if mood_val in ["happy", "excited"]: badges.append({"id": "mood", "name": "Positive Mood", "icon": "✨"})
                if score == 100: badges.append({"id": "day", "name": "Healthy Day", "icon": "🌟"})
                if score >= 80: badges.append({"id": "lifestyle", "name": "Healthy Life Style", "icon": "👑"})

                challenges = [
                    {"name": "Water Goal (8 cups)", "done": water_cups >= 8, "val": f"{water_cups}/8 cups"},
                    {"name": "Sleep Goal (8 hours)", "done": sleep_hours >= 8, "val": f"{sleep_hours}/8 hrs"},
                    {"name": "Activity Goal (8,000 steps)", "done": steps >= 8000, "val": f"{steps}/8000 steps"}
                ]

                return self.send_json({
                    "success": True,
                    "type": "daily",
                    "score": score,
                    "overall_status": rep.overall_status(score),
                    "metrics": {"water_cups": water_cups, "sleep_hours": sleep_hours, "steps": steps, "mood": mood_val},
                    "badges": badges,
                    "challenges": challenges
                })

            elif report_type == 'weekly':
                week_ago = datetime.combine(date.today() - timedelta(days=7), datetime.min.time())
                tw, sw, stw = 0, 0, 0
                wd, sd, ad = 0, 0, 0
                for item in water_data:
                    if str(item.get("user_id")) == str_uid:
                        try:
                            if datetime.strptime(item["date"], "%Y-%m-%d") >= week_ago: tw += item["cups"]; wd += 1
                        except ValueError: pass
                for item in sleep_data:
                    if str(item.get("user_id")) == str_uid:
                        try:
                            if datetime.strptime(item["date"], "%Y-%m-%d") >= week_ago: sw += item["hours"]; sd += 1
                        except ValueError: pass
                for item in activity_data:
                    if str(item.get("user_id")) == str_uid:
                        try:
                            if datetime.strptime(item["date"], "%Y-%m-%d") >= week_ago: stw += item["steps"]; ad += 1
                        except ValueError: pass

                avg_water = round(tw / wd, 1) if wd > 0 else 0
                avg_sleep = round(sw / sd, 1) if sd > 0 else 0
                avg_steps = round(stw / ad) if ad > 0 else 0
                score = rep.calculate_health_score(avg_water, avg_sleep, avg_steps, "happy")

                return self.send_json({
                    "success": True,
                    "type": "weekly",
                    "score": score,
                    "overall_status": rep.overall_status(score),
                    "averages": {"water_cups": avg_water, "sleep_hours": avg_sleep, "steps": avg_steps}
                })

            else: # monthly
                tm_water, tm_sleep, tm_steps = 0, 0, 0
                today = date.today()
                for item in water_data:
                    if str(item.get("user_id")) == str_uid:
                        try:
                            d = datetime.strptime(item["date"], "%Y-%m-%d")
                            if d.month == today.month and d.year == today.year: tm_water += item["cups"]
                        except ValueError: pass
                for item in sleep_data:
                    if str(item.get("user_id")) == str_uid:
                        try:
                            d = datetime.strptime(item["date"], "%Y-%m-%d")
                            if d.month == today.month and d.year == today.year: tm_sleep += item["hours"]
                        except ValueError: pass
                for item in activity_data:
                    if str(item.get("user_id")) == str_uid:
                        try:
                            d = datetime.strptime(item["date"], "%Y-%m-%d")
                            if d.month == today.month and d.year == today.year: tm_steps += item["steps"]
                        except ValueError: pass

                score = rep.calculate_monthly_score(tm_water, tm_sleep, tm_steps, "happy")
                return self.send_json({
                    "success": True,
                    "type": "monthly",
                    "score": score,
                    "overall_status": rep.overall_status(score),
                    "totals": {"water_cups": tm_water, "sleep_hours": tm_sleep, "steps": tm_steps}
                })

        self.send_error(404)

def run():
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, HealthAppHandler)
    print(f"Life Care Web App Server running on http://127.0.0.1:{PORT}")
    sys.stdout.flush()
    httpd.serve_forever()

if __name__ == '__main__':
    run()
