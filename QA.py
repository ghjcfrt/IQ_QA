import sqlite3
import tkinter as tk
from tkinter import messagebox

# 连接到 SQLite 数据库
conn = sqlite3.connect("test2.db")
cursor = conn.cursor()

# 如果表不存在则创建表
cursor.execute("""CREATE TABLE IF NOT EXISTS questions (
                    question TEXT NOT NULL,
                    answer_a TEXT NOT NULL,
                    answer_b TEXT NOT NULL,
                    answer_c TEXT NOT NULL,
                    answer_d TEXT NOT NULL,
                    right_answer TEXT NOT NULL)""")

# 如果表中没有数据则插入数据，否则不插入
cursor.execute("SELECT COUNT(*) FROM questions")
if cursor.fetchone()[0] == 0:  # 如果表中没有数据
    questions = [
        ("哈雷慧星的平均周期为？", "54年", "56年", "73年", "83年", "C"),
        ('夜郎自大中"夜郎"指的是现在哪个地方？', "贵州", "云南", "广西", "福建", "A"),
        ("在中国历史上是谁发明了麻药？", "孙思邈", "华佗", "张仲景", "扁鹊", "B"),
        ("京剧中花旦是指？", "年轻男子", "年轻女子", "年长男子", "年长女子", "B"),
        ("篮球比赛每队几人？", "4", "5", "6", "7", "B"),
        (
            "在天愿作比翼鸟,在地愿为连理枝,讲述的是谁的爱情故事？",
            "焦仲卿和刘兰芝",
            "梁山伯与祝英台",
            "崔莺莺和张生",
            "杨贵妃和唐明皇",
            "D",
        ),
    ]

    cursor.executemany(
        "INSERT INTO questions (question, answer_a, answer_b, answer_c, answer_d, right_answer) VALUES (?, ?, ?, ?, ?, ?)",
        questions,
    )

# 从数据库中获取问题
cursor.execute("SELECT * FROM questions")
values = cursor.fetchall()
conn.close()


class QuizApp:
    # 初始化函数
    def __init__(self, root):
        self.root = root
        self.root.title("智力问答游戏")
        self.score = 0
        self.current_question = 0

        self.question_label = tk.Label(root, text="智力问答测试", wraplength=400)
        self.question_label.pack(pady=20)

        self.var = tk.StringVar()

        # 修改单选按钮的创建逻辑
        self.options = [tk.Radiobutton(root, text="", variable=self.var, value=chr(65 + i)) for i in range(4)]
        for option in self.options:
            option.pack(anchor="center", pady=5)

        self.next_button = tk.Button(root, text="下一题", command=self.next_question)
        self.next_button.pack(pady=20)

        self.display_question()

    # 显示问题
    def display_question(self):
        if self.current_question < len(values):
            question = values[self.current_question]
            self.question_label.config(text=question[0])
            for i in range(4):
                self.options[i].config(text=question[i + 1], value=chr(65 + i))  # 设置选项文本及对应值

            self.var.set("")  # 清除之前的选择

        else:
            messagebox.showinfo("测验已完成", f"你的分数是 {self.score}")
            self.root.quit()

    # 下一题
    def next_question(self):
        if self.var.get().upper() == values[self.current_question][5].upper():
            self.score += 1
        self.current_question += 1
        self.display_question()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x300")
    app = QuizApp(root)
    root.mainloop()
