import tkinter as tk
from PIL import Image, ImageTk
import random

# 점수 초기화
score = 0
rounds_played = 0
max_rounds = 3

# 게임 선택지
choices = ['가위', '바위', '보']

# 이미지 로드
scissors_img = ImageTk.PhotoImage(Image.open("scissors.png").resize((100, 100)))
rock_img = ImageTk.PhotoImage(Image.open("rock.png").resize((100, 100)))
paper_img = ImageTk.PhotoImage(Image.open("paper.png").resize((100, 100)))

image_map = {
    '가위': scissors_img,
    '바위': rock_img,
    '보': paper_img
}

# GUI 설정
root = tk.Tk()
root.title("가위바위보 게임")
root.geometry("400x500")

# 결과 텍스트
result_label = tk.Label(root, text="게임을 시작하세요!", font=("Arial", 14))
result_label.pack(pady=10)

# 이미지 표시
user_img_label = tk.Label(root)
user_img_label.pack()

comp_img_label = tk.Label(root)
comp_img_label.pack()

# 점수 표시
score_label = tk.Label(root, text="현재 점수: 0", font=("Arial", 12))
score_label.pack(pady=10)

# 승패 판정 함수
def determine_winner(user, comp):
    if user == comp:
        return 0
    elif (user == '가위' and comp == '보') or \
         (user == '바위' and comp == '가위') or \
         (user == '보' and comp == '바위'):
        return 1
    else:
        return -1

# 게임 실행 함수
def play(user_choice):
    global score, rounds_played
    if rounds_played >= max_rounds:
        result_label.config(text="게임 종료! 최종 점수: {}".format(score))
        return

    comp_choice = random.choice(choices)
    user_img_label.config(image=image_map[user_choice])
    comp_img_label.config(image=image_map[comp_choice])

    result = determine_winner(user_choice, comp_choice)
    score += result
    rounds_played += 1

    if result == 1:
        result_text = "🎉 승리! 점수 +1"
    elif result == -1:
        result_text = "😢 패배... 점수 -1"
    else:
        result_text = "🤝 무승부! 점수 변동 없음"

    result_label.config(text=f"{rounds_played}번째 판 결과: {result_text}")
    score_label.config(text=f"현재 점수: {score}")

# 버튼 생성
for choice in choices:
    btn = tk.Button(root, text=choice, width=10, command=lambda c=choice: play(c))
    btn.pack(pady=5)

root.mainloop()
