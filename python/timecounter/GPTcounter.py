import PySimpleGUI as sg
import time
import threading

# GUIのレイアウト
layout = [
    [sg.Text("タイマー設定 (分):"), sg.InputText(size=(5, 1), key="-MINUTES-")],
    [sg.Button("スタート"), sg.Button("ストップ")],
    [sg.Text("", size=(15, 2), key="-TIMER-")],
]

# ウィンドウの生成
window = sg.Window("タイマーアプリ", layout, finalize=True)

# タイマーのカウントダウンフラグ
running = False

def update_timer_display(seconds):
    minutes, seconds = divmod(seconds, 60)
    window["-TIMER-"].update(f"残り時間: {minutes:02d}:{seconds:02d}")

def timer_thread(minutes):
    global running
    seconds = minutes * 60
    running = True
    while running and seconds > 0:
        update_timer_display(seconds)
        time.sleep(1)
        seconds -= 1
    if seconds <= 0:
        sg.popup("タイマーが終了しました！", title="タイマー終了")

# イベントループ
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == "スタート" and not running:
        minutes = int(values["-MINUTES-"])
        if minutes > 0:
            thread = threading.Thread(target=timer_thread, args=(minutes,))
            thread.daemon = True
            thread.start()
    if event == "ストップ" and running:
        running = False
        update_timer_display(0)

window.close()