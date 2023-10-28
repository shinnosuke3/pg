import tkinter as tk
from random import randint

def generate_numbers():
    num1.set(randint(10, 99))
    num2.set(randint(10, 99))
    result.set("")

def calculate_sum():
    result.set(num1.get() + num2.get())

def calculate_difference():
    result.set(num1.get() - num2.get())

# ウィンドウを作成
root = tk.Tk()
root.title("足し算・引き算勉強アプリ")

# 数字の変数を作成
num1 = tk.IntVar()
num2 = tk.IntVar()
result = tk.IntVar()

# ラベルを作成
label_num1 = tk.Label(root, textvariable=num1)
label_num2 = tk.Label(root, textvariable=num2)
label_result = tk.Label(root, textvariable=result)

# ボタンを作成
generate_button = tk.Button(root, text="新しい問題", command=generate_numbers)
sum_button = tk.Button(root, text="足し算", command=calculate_sum)
difference_button = tk.Button(root, text="引き算", command=calculate_difference)

# ウィジェットを配置
label_num1.pack()
label_num2.pack()
generate_button.pack()
sum_button.pack()
difference_button.pack()
label_result.pack()

generate_numbers()  # 最初の問題を生成

root.mainloop()
