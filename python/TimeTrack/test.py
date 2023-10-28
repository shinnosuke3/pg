import PySimpleGUI as sg
import datetime

class TimeTrackerApp:
    def __init__(self):
        self.tasks = {}
        self.current_task = None
        self.start_time = None

        self.layout = [
            [sg.Text('タスク名:'), sg.InputText(key='task_name'), sg.Button('Start'), sg.Button('Stop')],
            [sg.Button('History'), sg.Button('Report')],
            [sg.Multiline('', size=(40, 10), key='output')],
        ]

        self.window = sg.Window('タイムトラッキングアプリ', self.layout, finalize=True)

    def run(self):
        while True:
            event, values = self.window.read()
            if event == sg.WINDOW_CLOSED:
                break
            elif event == 'Start':
                self.start_task(values['task_name'])
            elif event == 'Stop':
                self.stop_task()
            elif event == 'History':
                self.show_history()
            elif event == 'Report':
                self.generate_report()

        self.window.close()

    def start_task(self, task_name):
        if task_name:
            self.current_task = task_name
            self.start_time = datetime.datetime.now()
            self.update_output(f'Started task: {task_name}')

    def stop_task(self):
        if self.current_task:
            end_time = datetime.datetime.now()
            elapsed_time = end_time - self.start_time
            if self.current_task in self.tasks:
                self.tasks[self.current_task] += elapsed_time
            else:
                self.tasks[self.current_task] = elapsed_time
            self.update_output(f'Stopped task: {self.current_task}')
            self.current_task = None

    def show_history(self):
        self.update_output('Task history:')
        for task, duration in self.tasks.items():
            self.update_output(f'{task}: {duration}')

    def generate_report(self):
        self.update_output('Task report:')
        for task, duration in self.tasks.items():
            self.update_output(f'{task}: {duration}')

    def update_output(self, text):
        current_text = self.window['output'].get()
        new_text = f'{current_text}{text}\n'
        self.window['output'].update(new_text)

if __name__ == '__main__':
    app = TimeTrackerApp()
    app.run()

