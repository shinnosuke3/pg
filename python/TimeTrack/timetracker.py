import tkinter as tk
import time
import json

class TimeTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Tracker")

        self.tasks = []
        self.load_data()

        self.current_task = None
        self.start_time = None

        self.task_label = tk.Label(root, text="Task Name:")
        self.task_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

        self.task_entry = tk.Entry(root)
        self.task_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

        self.start_button = tk.Button(root, text="Start", command=self.start_task)
        self.start_button.grid(row=0, column=2, padx=10, pady=5)

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_task)
        self.stop_button.grid(row=0, column=3, padx=10, pady=5)
        self.stop_button.config(state=tk.DISABLED)

        self.report_button = tk.Button(root, text="Show Report", command=self.display_report)
        self.report_button.grid(row=1, column=0, padx=10, pady=5, columnspan=2)

        self.history_button = tk.Button(root, text="Show History", command=self.display_history)
        self.history_button.grid(row=1, column=2, padx=10, pady=5, columnspan=2)

        self.quit_button = tk.Button(root, text="Quit", command=self.root.quit)
        self.quit_button.grid(row=3, column=0, padx=10, pady=5, columnspan=4)

        self.recent_history_frame = tk.Frame(root)
        self.recent_history_frame.grid(row=4, column=0, padx=10, pady=5, columnspan=4)

        self.create_recent_history_widgets()

    def start_task(self):
        if self.current_task:
            self.stop_task()
        task_name = self.task_entry.get().strip()  # 空白を削除してタスク名を取得
        if task_name:
            if not self.is_task_in_progress(task_name):
                self.current_task = {"name": task_name, "start_time": time.time(), "end_time": None}
                self.start_time = time.time()
                self.stop_button.config(state=tk.NORMAL)
                self.start_button.config(state=tk.DISABLED)
                self.task_entry.config(state=tk.DISABLED)
            else:
                self.show_error_message(f"Task '{task_name}' is already in progress.")
        else:
            self.show_error_message("Task name cannot be empty.")

    def stop_task(self):
        if self.current_task:
            self.current_task["end_time"] = time.time()
            self.tasks.append(self.current_task)
            self.save_data()
            self.current_task = None
            self.stop_button.config(state=tk.DISABLED)
            self.start_button.config(state=tk.NORMAL)
            self.task_entry.config(state=tk.NORMAL)
            self.update_recent_history()

    def display_report(self):
        report_window = tk.Toplevel(self.root)
        report_window.title("Task Report")

        report_text = "Task Report:\n"
        for task_name, task_time in self.get_task_times().items():
            report_text += f"{task_name}: {task_time:.2f} seconds\n"

        report_label = tk.Label(report_window, text=report_text)
        report_label.pack()

    def display_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("Session History")

        for i, session in enumerate(reversed(self.tasks[-10:])):  # 最新の10セッションを取得
            task_name = session["name"]
            start_date = time.strftime("%Y-%m-%d", time.localtime(session["start_time"]))
            end_time = time.strftime("%H:%M", time.localtime(session["end_time"]))
            session_time = session["end_time"] - session["start_time"]

            delete_button = tk.Button(history_window, text="Delete", command=lambda idx=i: self.delete_session(idx))
            delete_button.grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)

            history_text = f"Task: {task_name}, Date: {start_date}, End Time: {end_time}, Duration: {session_time:.2f} seconds\n"
            history_label = tk.Label(history_window, text=history_text)
            history_label.grid(row=i, column=1, padx=5, pady=5, sticky=tk.W)

    def delete_session(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_data()
            self.display_history()
            self.update_recent_history()

    def create_recent_history_widgets(self):
        self.recent_history_labels = []

        for i in range(5):
            label = tk.Label(self.recent_history_frame, text="", anchor=tk.W)
            label.grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)
            self.recent_history_labels.append(label)

        self.update_recent_history()

    def update_recent_history(self):
        recent_sessions = self.tasks[-5:]  # 直近の5つのセッションを取得
        for i, session in enumerate(reversed(recent_sessions)):
            task_name = session["name"]
            start_date = time.strftime("%Y-%m-%d %H:%M", time.localtime(session["start_time"]))
            end_date = time.strftime("%Y-%m-%d %H:%M", time.localtime(session["end_time"]))
            session_time = session["end_time"] - session["start_time"]
            self.recent_history_labels[i].config(text=f"{task_name} ({start_date} - {end_date}), Duration: {session_time:.2f} seconds")

    def is_task_in_progress(self, task_name):
        return bool(self.current_task and self.current_task["name"] == task_name)

    def get_task_times(self):
        task_times = {}
        for task in self.tasks:
            task_name = task["name"]
            task_time = task["end_time"] - task["start_time"]
            if task_name in task_times:
                task_times[task_name] += task_time
            else:
                task_times[task_name] = task_time
        return task_times

    def show_error_message(self, message):
        error_window = tk.Toplevel(self.root)
        error_window.title("Error")
        error_label = tk.Label(error_window, text=message)
        error_label.pack()
        ok_button = tk.Button(error_window, text="OK", command=error_window.destroy)
        ok_button.pack()

    def load_data(self):
        try:
            with open("tasks.json", "r") as file:
                self.tasks = json.load(file)
        except FileNotFoundError:
            self.tasks = []

    def save_data(self):
        with open("tasks.json", "w") as file:
            json.dump(self.tasks, file)

if __name__ == "__main__":
    root = tk.Tk()
    app = TimeTrackerApp(root)
    root.mainloop()
