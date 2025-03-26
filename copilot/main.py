import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Pillow 라이브러리 사용
import random
import os

class GomokuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("오목게임")
        self.root.geometry("640x640")  # 창 크기 고정

        # 게임 상태
        self.board_size = 19  # 19x19 바둑판
        self.cell_size = 30   # 각 셀의 크기 (창 크기에 맞게 조정)
        self.board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = "black"  # 현재 플레이어 ("black" 또는 "white")
        self.timer_label = None  # 타이머 표시 라벨
        self.time_left = 30  # 남은 시간 (초)

        # 메인 화면 표시
        self.show_main_menu()

    def show_main_menu(self):
        """메인 메뉴를 표시합니다."""
        # 기존 위젯 제거
        for widget in self.root.winfo_children():
            widget.destroy()

        # Canvas 생성
        self.canvas = tk.Canvas(self.root, width=640, height=640)
        self.canvas.pack(fill="both", expand=True)

        # 배경 이미지 추가
        try:
            # 절대 경로로 이미지 파일 경로 설정
            image_path = r"c:\Codingdingding\copilot\images\omok.png"
            print(f"이미지 경로: {image_path}")  # 디버깅 메시지
            bg_image = Image.open(image_path)
            bg_image = bg_image.resize((640, 640), Image.Resampling.LANCZOS)  # 최신 Pillow에서 사용
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        except Exception as e:
            print(f"이미지를 불러올 수 없습니다: {e}")  # 에러 메시지 출력

        # 게임 제목
        title = tk.Label(self.root, text="오목게임", font=("Arial", 24), bg="white", fg="black")
        title.place(relx=0.5, rely=0.2, anchor="center")

        # 버튼 프레임 (중앙 정렬)
        button_frame = tk.Frame(self.root, bg="white")
        button_frame.place(relx=0.5, rely=0.5, anchor="center")

        # 게임 시작 버튼
        start_button = tk.Button(button_frame, text="게임 시작", font=("Arial", 16), command=self.start_game, width=15)
        start_button.pack(pady=10)

        # 게임 종료 버튼
        exit_button = tk.Button(button_frame, text="게임 종료", font=("Arial", 16), command=self.exit_game, width=15)
        exit_button.pack(pady=10)

    def start_game(self):
        """게임을 시작합니다."""
        # 기존 위젯 제거
        for widget in self.root.winfo_children():
            widget.destroy()

        # 바둑판 그리기
        self.canvas = tk.Canvas(self.root, width=self.board_size * self.cell_size, height=self.board_size * self.cell_size, bg="beige")
        self.canvas.pack()

        # 바둑판 선 그리기
        self.draw_board()

        # 타이머 표시
        self.timer_label = tk.Label(self.root, text=f"남은 시간: {self.time_left}초", font=("Arial", 16))
        self.timer_label.pack(pady=10)

        # 타이머 시작
        self.start_timer()

        # 클릭 이벤트 바인딩
        self.canvas.bind("<Button-1>", self.place_stone)

    def draw_board(self):
        """바둑판의 선을 그립니다."""
        for i in range(self.board_size):
            # 가로선
            self.canvas.create_line(self.cell_size // 2, self.cell_size // 2 + i * self.cell_size,
                                     self.board_size * self.cell_size - self.cell_size // 2, self.cell_size // 2 + i * self.cell_size)
            # 세로선
            self.canvas.create_line(self.cell_size // 2 + i * self.cell_size, self.cell_size // 2,
                                     self.cell_size // 2 + i * self.cell_size, self.board_size * self.cell_size - self.cell_size // 2)

    def start_timer(self):
        """타이머를 시작합니다."""
        # 기존 타이머가 실행 중이면 중단
        if hasattr(self, "timer_id"):
            self.root.after_cancel(self.timer_id)
        self.time_left = 30
        self.update_timer()

    def update_timer(self):
        """타이머를 업데이트합니다."""
        if self.time_left > 0:
            self.timer_label.config(text=f"남은 시간: {self.time_left}초")
            self.time_left -= 1
            # 정확히 1초 후에 update_timer를 호출
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            # 시간이 초과되면 랜덤으로 돌을 놓음
            self.place_random_stone()

    def place_random_stone(self):
        """랜덤한 위치에 돌을 놓습니다."""
        empty_positions = [(r, c) for r in range(self.board_size) for c in range(self.board_size) if self.board[r][c] is None]
        if empty_positions:
            row, col = random.choice(empty_positions)
            self.place_stone_at(row, col)

    def place_stone(self, event):
        """돌을 놓는 로직을 처리합니다."""
        # 클릭한 위치를 바둑판 좌표로 변환
        col = round((event.x - self.cell_size // 2) / self.cell_size)
        row = round((event.y - self.cell_size // 2) / self.cell_size)

        # 유효한 위치인지 확인
        if 0 <= row < self.board_size and 0 <= col < self.board_size and self.board[row][col] is None:
            self.place_stone_at(row, col)

            # 타이머 초기화
            if hasattr(self, "timer_id"):
                self.root.after_cancel(self.timer_id)  # 기존 타이머 중단
            self.start_timer()

    def place_stone_at(self, row, col):
        """지정된 위치에 돌을 놓습니다."""
        # 돌을 놓음
        x = col * self.cell_size + self.cell_size // 2
        y = row * self.cell_size + self.cell_size // 2
        color = self.current_player
        self.canvas.create_oval(
            x - self.cell_size // 4, y - self.cell_size // 4,
            x + self.cell_size // 4, y + self.cell_size // 4,
            fill=color
        )
        self.board[row][col] = self.current_player

        # 승리 조건 확인
        if self.check_winner(row, col):
            messagebox.showinfo("Game Over", f"{self.current_player.capitalize()} wins!")
            self.reset_game()
            return

        # 플레이어 전환
        self.current_player = "white" if self.current_player == "black" else "black"

        # 타이머 재시작
        self.start_timer()

    def check_winner(self, row, col):
        """승리 조건을 확인합니다."""
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # 가로, 세로, 대각선 방향
        for dx, dy in directions:
            count = 1
            count += self.count_stones(row, col, dx, dy)
            count += self.count_stones(row, col, -dx, -dy)
            if count >= 5:
                return True
        return False

    def count_stones(self, row, col, dx, dy):
        """특정 방향으로 연속된 돌의 개수를 셉니다."""
        count = 0
        player = self.board[row][col]
        for _ in range(4):  # 최대 4칸 확인
            row += dy
            col += dx
            if 0 <= row < self.board_size and 0 <= col < self.board_size and self.board[row][col] == player:
                count += 1
            else:
                break
        return count

    def reset_game(self):
        """게임을 초기화합니다."""
        self.board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = "black"
        self.show_main_menu()

    def exit_game(self):
        """게임을 종료합니다."""
        self.root.quit()

def main():
    root = tk.Tk()
    app = GomokuApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()