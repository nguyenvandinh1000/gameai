import tkinter as tk
import random
import heapq

BOARD_WIDTH = 800
BOARD_HEIGHT = 600
CELL_SIZE = 20
TARGET_SCORE = 50
MOVE_SPEED = 200

class SnakeGame:
    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    def astar(self, start, targets):
        directions = {
            "Up": (0, -CELL_SIZE),
            "Down": (0, CELL_SIZE),
            "Left": (-CELL_SIZE, 0),
            "Right": (CELL_SIZE, 0)
        }

        open_list = []
        heapq.heappush(open_list, (0, 0, start, []))

        visited = set()

        while open_list:
            f, g, current, path = heapq.heappop(open_list)

            if current in visited:
                continue
            visited.add(current)

            if current in targets:
                return path

            for d, (dx, dy) in directions.items():
                nx, ny = current[0] + dx, current[1] + dy
                new_pos = (nx, ny)

                if new_pos in visited:
                    continue

                # check an toàn
                if nx < 0 or nx >= BOARD_WIDTH or ny < 0 or ny >= BOARD_HEIGHT:
                    continue
                if new_pos in self.snake2[:-1]:
                    continue
                if new_pos in self.snake[:-1]:
                    continue

                # chọn táo gần nhất để tính heuristic
                nearest = min(targets, key=lambda t: self.heuristic(new_pos, t))

                g_new = g + 1
                h_new = self.heuristic(new_pos, nearest)
                f_new = g_new + h_new

                heapq.heappush(open_list, (f_new, g_new, new_pos, path + [d]))

        return []
    def __init__(self, root):
        self.root = root
        root.title("Rắn săn mồi")

        self.top_frame = tk.Frame(root, bg="#80c2f2")
        self.top_frame.pack(fill=tk.X)

        self.target_label = tk.Label(self.top_frame, text=f"TARGET: {TARGET_SCORE} 🍎", font=("Consolas", 16), bg="#80c2f2")
        self.target_label.pack(side=tk.LEFT, padx=10, pady=8)

        self.score_label = tk.Label(self.top_frame, text="P1: 0 🍎", font=("Consolas", 16), bg="#80c2f2")
        self.score_label.pack(side=tk.LEFT, padx=10)

        self.best_label = tk.Label(self.top_frame, text="P2: 0 🍎", font=("Consolas", 16), bg="#80c2f2")
        self.best_label.pack(side=tk.LEFT, padx=10)

        
        self.canvas = tk.Canvas(root, width=BOARD_WIDTH, height=BOARD_HEIGHT, bg="#b7f26b", highlightthickness=5, highlightbackground="black")
        self.canvas.pack()

        self.root.bind("<Up>", lambda event: self.change_direction("Up"))
        self.root.bind("<Down>", lambda event: self.change_direction("Down"))
        self.root.bind("<Left>", lambda event: self.change_direction("Left"))
        self.root.bind("<Right>", lambda event: self.change_direction("Right"))

        self.root.bind("<w>", lambda event: self.change_direction2("Up"))
        self.root.bind("<s>", lambda event: self.change_direction2("Down"))
        self.root.bind("<a>", lambda event: self.change_direction2("Left"))
        self.root.bind("<d>", lambda event: self.change_direction2("Right"))

        self.game_mode = None  # "pvp" or "pve"
        self.reset_game()
        self.show_main_menu()

    def reset_game(self):
        self.canvas.delete("all")
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = "Right"
        self.snake2 = [(500, 300), (520, 300), (540, 300)]
        self.direction2 = "Left"
        self.score = 0
        self.score2 = 0
        self.best_score = 0
        self.game_active = False
        self.apples = []
        self.update_labels()

    def start_game(self):
        self.show_main_menu()

    def show_main_menu(self):
        self.canvas.delete("all")
        
        # Title
        self.canvas.create_text(BOARD_WIDTH // 2, 50, text="Snake", font=("Consolas", 48, "bold"), fill="#0066ff")
        
        # PLAY button
        self.canvas.create_rectangle(275, 150, 525, 210, fill="#0033cc", outline="#0033cc")
        self.canvas.create_text(400, 180, text="PLAY", font=("Consolas", 28, "bold"), fill="red")
        self.canvas.tag_bind("play_btn", "<Button-1>", lambda e: self.show_options())
        self.canvas.create_rectangle(275, 150, 525, 210, tags="play_btn", fill="", outline="")
        
        # EXIT button
        self.canvas.create_rectangle(275, 260, 525, 320, fill="#0033cc", outline="#0033cc")
        self.canvas.create_text(400, 290, text="EXIT", font=("Consolas", 28, "bold"), fill="red")
        self.canvas.tag_bind("exit_btn", "<Button-1>", lambda e: self.root.quit())
        self.canvas.create_rectangle(275, 260, 525, 320, tags="exit_btn", fill="", outline="")

    def show_options(self):
        self.canvas.delete("all")
        
        # Title
        self.canvas.create_text(BOARD_WIDTH // 2, 50, text="OPTIONS", font=("Consolas", 36, "bold"), fill="#0066ff")
        
        # PVP button
        self.canvas.create_rectangle(250, 150, 450, 230, fill="#0033cc", outline="#0033cc")
        self.canvas.create_text(350, 190, text="PVP", font=("Consolas", 32, "bold"), fill="red")
        self.canvas.tag_bind("pvp_btn", "<Button-1>", lambda e: self.start_pvp())
        self.canvas.create_rectangle(250, 150, 450, 230, tags="pvp_btn", fill="", outline="")
        
        # PVE button
        self.canvas.create_rectangle(450, 150, 650, 230, fill="#0033cc", outline="#0033cc")
        self.canvas.create_text(550, 190, text="PVE", font=("Consolas", 32, "bold"), fill="red")
        self.canvas.tag_bind("pve_btn", "<Button-1>", lambda e: self.start_pve())
        self.canvas.create_rectangle(450, 150, 650, 230, tags="pve_btn", fill="", outline="")
        
        # BACK button
        self.canvas.create_rectangle(275, 300, 525, 360, fill="#0033cc", outline="#0033cc")
        self.canvas.create_text(400, 330, text="BACK", font=("Consolas", 24, "bold"), fill="red")
        self.canvas.tag_bind("back_btn", "<Button-1>", lambda e: self.show_main_menu())
        self.canvas.create_rectangle(275, 300, 525, 360, tags="back_btn", fill="", outline="")

    def start_pvp(self):
        self.game_mode = "pvp"
        self.start_game_mode()

    def start_pve(self):
        self.game_mode = "pve"
        self.start_game_mode()

    def start_game_mode(self):
        self.canvas.delete("all")
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = "Right"
        self.snake2 = [(500, 300), (520, 300), (540, 300)]
        self.direction2 = "Left"
        self.score = 0
        self.score2 = 0
        self.game_active = True
        self.place_apples()
        self.update_labels()
        self.draw_board()
        self.move_snake()

    def place_apples(self):
        self.apples = []
        while len(self.apples) < 3:
            x = random.randrange(0, BOARD_WIDTH, CELL_SIZE)
            y = random.randrange(0, BOARD_HEIGHT, CELL_SIZE)
            apple = (x, y)
            if apple not in self.snake and apple not in self.snake2 and apple not in self.apples:
                self.apples.append(apple)

    def draw_board(self):
        self.canvas.delete("snake")
        self.canvas.delete("apple")

        for x, y in self.snake:
            self.canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, fill="#7c7c7c", outline="#2a2a2a", tags="snake")

        for x, y in self.snake2:
            self.canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, fill="#0066ff", outline="#0033aa", tags="snake")

        for ax, ay in self.apples:
            self.canvas.create_oval(ax + 2, ay + 2, ax + CELL_SIZE - 2, ay + CELL_SIZE - 2, fill="red", tags="apple")

    def change_direction(self, new_direction):
        opposite = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
        if self.game_active and new_direction != opposite.get(self.direction):
            self.direction = new_direction

    def change_direction2(self, new_direction):
        opposite = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
        if self.game_active and new_direction != opposite.get(self.direction2):
            self.direction2 = new_direction

    def ai_move(self):
        if not self.apples:
            return

        head = self.snake2[0]

        path = self.astar(head, set(self.apples))

        if path:
            self.direction2 = path[0]
        else:
            self.random_safe_move()
    def random_safe_move(self):
        directions = {
            "Up": (0, -CELL_SIZE),
            "Down": (0, CELL_SIZE),
            "Left": (-CELL_SIZE, 0),
            "Right": (CELL_SIZE, 0)
        }

        head_x, head_y = self.snake2[0]

        for d, (dx, dy) in directions.items():
            nx, ny = head_x + dx, head_y + dy
            pos = (nx, ny)

            if 0 <= nx < BOARD_WIDTH and 0 <= ny < BOARD_HEIGHT \
            and pos not in self.snake2 and pos not in self.snake:
                self.direction2 = d
                return

    def move_snake(self):
        if not self.game_active:
            return

        # Move snake 1
        head_x, head_y = self.snake[0]
        if self.direction == "Up":
            head_y -= CELL_SIZE
        elif self.direction == "Down":
            head_y += CELL_SIZE
        elif self.direction == "Left":
            head_x -= CELL_SIZE
        elif self.direction == "Right":
            head_x += CELL_SIZE

        new_head = (head_x, head_y)
        self.snake.insert(0, new_head)

        if new_head in self.apples:
            self.apples.remove(new_head)
            self.score += 1
            if len(self.apples) == 0:
                self.place_apples()
            if self.score >= TARGET_SCORE:
                self.game_won(1)
                return
        else:
            self.snake.pop()
        if self.game_mode == "pve":
            self.ai_move()
        # Move snake 2
        head_x, head_y = self.snake2[0]
        if self.direction2 == "Up":
            head_y -= CELL_SIZE
        elif self.direction2 == "Down":
            head_y += CELL_SIZE
        elif self.direction2 == "Left":
            head_x -= CELL_SIZE
        elif self.direction2 == "Right":
            head_x += CELL_SIZE

        new_head2 = (head_x, head_y)
        self.snake2.insert(0, new_head2)

        if new_head2 in self.apples:
            self.apples.remove(new_head2)
            self.score2 += 1
            if len(self.apples) == 0:
                self.place_apples()
            if self.score2 >= TARGET_SCORE:
                self.game_won(2)
                return
        else:
            self.snake2.pop()
        if new_head == new_head2:
            self.game_over()
            return
        # Check collisions
        if self.check_collision(new_head, self.snake):
            self.game_won(2)
            return

        if self.check_collision(new_head2, self.snake2):
            self.game_won(1)
            return

        # Check if snakes hit each other
        if new_head in self.snake2[:-1]:
            self.game_won(2)
            return

        if new_head2 in self.snake[:-1]:
            self.game_won(1)
            return

        self.draw_board()
        self.update_labels()
        self.root.after(MOVE_SPEED, self.move_snake)

    def check_collision(self, head, snake):
        x, y = head
        if x < 0 or x >= BOARD_WIDTH or y < 0 or y >= BOARD_HEIGHT:
            return True
        if head in snake[1:]:
            return True
        return False

    def game_over(self):
        self.game_active = False
        self.update_labels()
        self.canvas.create_text(BOARD_WIDTH // 2, BOARD_HEIGHT // 2, text="GAME OVER", font=("Consolas", 32, "bold"), fill="darkred")

    def game_won(self, player):
        self.game_active = False
        self.update_labels()
        self.show_end_screen(player)

    def show_end_screen(self, player):
        self.canvas.delete("all")
        
        # Winner text
        winner_text = f"P{player} WIN"
        self.canvas.create_text(BOARD_WIDTH // 2, 60, text=winner_text, font=("Consolas", 48, "bold"), fill="red")
        
        # Score display
        score_text = f"SCORE: P1- {self.score}PTS\nP2- {self.score2}PTS"
        self.canvas.create_text(BOARD_WIDTH // 2, 150, text=score_text, font=("Consolas", 20, "bold"), fill="red")
        
        # RETRY button
        self.canvas.create_rectangle(60, 250, 240, 320, fill="#0033cc", outline="#0033cc")
        self.canvas.create_text(150, 285, text="RETRY", font=("Consolas", 24, "bold"), fill="red")
        self.canvas.tag_bind("retry_btn", "<Button-1>", lambda e: self.start_game())
        self.canvas.tag_lower("retry_btn")
        self.canvas.create_rectangle(60, 250, 240, 320, tags="retry_btn", fill="", outline="")
        
        # QUIT button
        self.canvas.create_rectangle(360, 250, 540, 320, fill="#0033cc", outline="#0033cc")
        self.canvas.create_text(450, 285, text="QUIT", font=("Consolas", 24, "bold"), fill="red")
        self.canvas.tag_bind("quit_btn", "<Button-1>", lambda e: self.root.quit())
        self.canvas.tag_lower("quit_btn")
        self.canvas.create_rectangle(360, 250, 540, 320, tags="quit_btn", fill="", outline="")

    def update_labels(self):
        self.score_label.config(text=f"P1 (↑↓←→): {self.score} 🍎")
        self.best_label.config(text=f"P2 (WASD): {self.score2} 🍎")

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()