import os
import subprocess
import datetime
import json

class WinUpdaterPro:
    def __init__(self):
        self.update_log = "update_log.json"
        self.load_update_log()

    def load_update_log(self):
        if os.path.exists(self.update_log):
            with open(self.update_log, 'r') as file:
                self.update_schedule = json.load(file)
        else:
            self.update_schedule = {}
    
    def save_update_log(self):
        with open(self.update_log, 'w') as file:
            json.dump(self.update_schedule, file, indent=4)

    def check_for_updates(self):
        print("Checking for updates...")
        subprocess.run(["powershell", "Get-WindowsUpdate"])
    
    def schedule_update(self, update_name, date_time):
        if update_name in self.update_schedule:
            print(f"Update '{update_name}' is already scheduled.")
            return
        
        self.update_schedule[update_name] = date_time
        self.save_update_log()
        print(f"Scheduled update '{update_name}' for {date_time}.")

    def view_scheduled_updates(self):
        if not self.update_schedule:
            print("No updates scheduled.")
            return
        
        print("Scheduled Updates:")
        for update, time in self.update_schedule.items():
            print(f" - {update} at {time}")

    def install_updates(self):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        updates_to_install = [upd for upd, time in self.update_schedule.items() if time <= current_time]
        
        if not updates_to_install:
            print("No updates to install at this time.")
            return

        for update in updates_to_install:
            print(f"Installing update: {update}")
            # Simulate installation
            subprocess.run(["powershell", f"Install-WindowsUpdate -KBArticleID {update}"])
            del self.update_schedule[update]
        
        self.save_update_log()

    def main_menu(self):
        while True:
            print("\nWinUpdaterPro Main Menu")
            print("1. Check for Updates")
            print("2. Schedule an Update")
            print("3. View Scheduled Updates")
            print("4. Install Due Updates")
            print("5. Exit")

            choice = input("Select an option: ")

            if choice == '1':
                self.check_for_updates()
            elif choice == '2':
                update_name = input("Enter update name (KBxxxxxxx): ")
                date_time = input("Enter date and time to schedule (YYYY-MM-DD HH:MM:SS): ")
                self.schedule_update(update_name, date_time)
            elif choice == '3':
                self.view_scheduled_updates()
            elif choice == '4':
                self.install_updates()
            elif choice == '5':
                print("Exiting WinUpdaterPro.")
                break
            else:
                print("Invalid option. Please try again.")

if __name__ == "__main__":
    win_updater_pro = WinUpdaterPro()
    win_updater_pro.main_menu()