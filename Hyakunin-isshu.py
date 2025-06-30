import tkinter as tk
from tkinter import PhotoImage
import random
import os
import csv

IMAGE_DIR = "images"
IMAGE_PREFIX = "f1s1_"
IMAGE_EXT = ".png"

class HyakuninIsshuApp:
    def __init__(self, master):
        self.master = master
        master.title("百人一首")
        master.configure(bg="#404040")

        # CSV読み込み
        self.karuta = self.load_karuta("karuta.csv")
        self.numbers = list(self.karuta.keys())

        # 状態
        self.correct = 0
        self.total = 0
        self.correct_id = None

        # 上の句ラベル
        self.ku_label = tk.Label(master, text="上の句：", fg="white", bg="#404040", font=("Helvetica", 14))
        self.ku_label.pack()
        self.upper_ku = tk.Label(master, text="", fg="white", bg="#404040", font=("Helvetica", 16))
        self.upper_ku.pack()

        # 画像ボタン
        self.frame = tk.Frame(master, bg="#404040")
        self.frame.pack()

        self.buttons = []
        self.images = []
        for i in range(6):
            dummy = PhotoImage(file=os.path.join(IMAGE_DIR, f"{IMAGE_PREFIX}001{IMAGE_EXT}"))
            self.images.append(dummy)
            btn = tk.Button(self.frame, image=dummy, command=lambda i=i: self.check_answer(i))
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(btn)

        # 正答数・正答率
        self.count_label = tk.Label(master, text="正答数:0", fg="white", bg="#404040")
        self.count_label.pack()
        self.per_label = tk.Label(master, text="正答率:0%", fg="white", bg="#404040")
        self.per_label.pack()

        # 正誤判定ラベル
        self.judge_label = tk.Label(master, text="", fg="white", bg="#404040", font=("Helvetica", 14))
        self.judge_label.pack(pady=5)

        # 操作ボタン
        self.start_button = tk.Button(master, text="開始", command=self.start_quiz)
        self.start_button.pack(side=tk.LEFT, padx=5, pady=10)
        self.reset_button = tk.Button(master, text="リセット", command=self.reset)
        self.reset_button.pack(side=tk.LEFT, padx=5, pady=10)
        self.exit_button = tk.Button(master, text="終了", command=master.quit)
        self.exit_button.pack(side=tk.LEFT, padx=5, pady=10)

    def load_karuta(self, csv_file):
        karuta = {}
        with open(csv_file, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                karuta[int(row['id'])] = {
                    'upper_ku': row['upper_ku'],
                    'lower_ku': row['lower_ku']
                }
        return karuta

    def start_quiz(self):
        self.correct_id = random.choice(self.numbers)
        self.upper_ku.config(text=self.karuta[self.correct_id]['upper_ku'])

        choices = random.sample([x for x in self.numbers if x != self.correct_id], 5)
        all_choices = [self.correct_id] + choices
        random.shuffle(all_choices)

        for i in range(6):
            path = os.path.join(IMAGE_DIR, f"{IMAGE_PREFIX}{all_choices[i]:03}{IMAGE_EXT}")
            img = PhotoImage(file=path)
            self.images[i] = img
            self.buttons[i].config(image=img)
            self.buttons[i].image = img  # GC防止
            self.buttons[i].config(command=lambda num=all_choices[i]: self.check_answer(num))

    def check_answer(self, selected):
        if self.correct_id is None:
            self.judge_label.config(text="問題を開始してください！")
            return

        self.total += 1
        if selected == self.correct_id:
            self.correct += 1
            self.judge_label.config(text="正解！")
        else:
            correct_upper = self.karuta[self.correct_id]['upper_ku']
            correct_lower = self.karuta[self.correct_id]['lower_ku']
            self.judge_label.config(
                text=f"不正解！ 正解は:\n{correct_upper}\n{correct_lower}"
            )

        per = (self.correct / self.total) * 100 if self.total else 0
        self.count_label.config(text=f"正答数:{self.correct}")
        self.per_label.config(text=f"正答率:{per:.1f}%")

        self.master.after(1500, self.start_quiz)

    def reset(self):
        self.correct = 0
        self.total = 0
        self.correct_id = None
        self.upper_ku.config(text="")
        self.count_label.config(text="正答数:0")
        self.per_label.config(text="正答率:0%")
        self.judge_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = HyakuninIsshuApp(root)
    root.mainloop()
