import tkinter as tk
from tkinter import ttk
import math, random, threading, time
from PIL import Image, ImageTk, ImageDraw

ROWS, COLS = 6, 7
EMPTY, PLAYER, AI = 0, 1, 2
SQUARE = 80
WIDTH, HEIGHT = COLS * SQUARE, ROWS * SQUARE
DIFFICULTY = {"Easy":2, "Medium":4, "Hard":6}


def create_board():
    return [[EMPTY] * COLS for _ in range(ROWS)]


def valid_cols(b):
    return [c for c in range(COLS) if b[0][c] == EMPTY]


def next_row(b, c):
    for r in range(ROWS - 1, -1, -1):
        if b[r][c] == EMPTY: return r


def winning_line(b, p):
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(b[r][c + i] == p for i in range(4)): return [(r, c + i) for i in range(4)]
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(b[r + i][c] == p for i in range(4)): return [(r + i, c) for i in range(4)]
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(b[r + i][c + i] == p for i in range(4)): return [(r + i, c + i) for i in range(4)]
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(b[r - i][c + i] == p for i in range(4)): return [(r - i, c + i) for i in range(4)]
    return None


def is_terminal(b):
    return bool(winning_line(b, PLAYER) or winning_line(b, AI) or not valid_cols(b))


def evaluate_window(win, p):
    opp = PLAYER if p == AI else AI
    if win.count(p) == 4: return 100
    if win.count(p) == 3 and win.count(EMPTY) == 1: return 5
    if win.count(p) == 2 and win.count(EMPTY) == 2: return 2
    if win.count(opp) == 3 and win.count(EMPTY) == 1: return -4
    return 0


def score_pos(b, p):
    score = 0
    center = [b[r][COLS // 2] for r in range(ROWS)]
    score += center.count(p) * 3
    for r in range(ROWS):
        for c in range(COLS - 3):
            score += evaluate_window(b[r][c:c + 4], p)
    for c in range(COLS):
        colarr = [b[r][c] for r in range(ROWS)]
        for r in range(ROWS - 3):
            score += evaluate_window(colarr[r:r + 4], p)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            d1 = [b[r + i][c + i] for i in range(4)]
            d2 = [b[r + 3 - i][c + i] for i in range(4)]
            score += evaluate_window(d1, p) + evaluate_window(d2, p)
    return score


def minimax(b, depth, alpha, beta, maximizing):
    valid = valid_cols(b)
    term = is_terminal(b)
    if depth == 0 or term:
        if term:
            if winning_line(b, AI): return None, math.inf
            if winning_line(b, PLAYER):return None, -math.inf
            return None, 0
        return None, score_pos(b, AI)
    if maximizing:
        val, best = -math.inf, random.choice(valid)
        for c in valid:
            r = next_row(b, c); b[r][c] = AI
            _, sc = minimax(b, depth - 1, alpha, beta, False)
            b[r][c] = EMPTY
            if sc > val: val, best = sc, c
            alpha = max(alpha, val)
            if alpha >= beta: break
        return best, val
    else:
        val, best = math.inf, random.choice(valid)
        for c in valid:
            r = next_row(b, c); b[r][c] = PLAYER
            _, sc = minimax(b, depth - 1, alpha, beta, True)
            b[r][c] = EMPTY
            if sc < val: val, best = sc, c
            beta = min(beta, val)
            if alpha >= beta: break
        return best, val


class Connect4:

    def _init_(self):
        self.root = tk.Tk()
        self.root.title("Connect 4")
        self.root.geometry(f"{WIDTH+40}x{HEIGHT+250}")
        self.root.configure(bg="#d0f0ea")
        self._make_circles()
        self._build_landing()
        self._build_game()
        self.board = create_board()
        self.turn = PLAYER
        self.game_over = False
        self.landing.pack(fill="both", expand=True)
        self.root.mainloop()

    def _make_circles(self):
        hr = SQUARE * 8; pad = hr // 80

        def mk(color):
            img = Image.new("RGBA", (hr, hr), (0, 0, 0, 0))
            d = ImageDraw.Draw(img)
            d.ellipse((pad, pad, hr - pad, hr - pad), fill=color)
            return ImageTk.PhotoImage(img.resize((SQUARE, SQUARE), Image.LANCZOS))

        self.hole = mk("white"); self.red = mk("#E63946"); self.yellow = mk("#F4D35E")

    def _build_landing(self):
        f = self.landing = tk.Frame(self.root, bg="#d0f0ea")
        header, textf, labf, btnf = ("Segoe UI", 36, "bold"), ("Segoe UI", 14), ("Segoe UI", 12), ("Segoe UI", 14, "bold")
        tk.Label(f, text="Connect 4", font=header, bg="#d0f0ea").pack(pady=(20, 5))
        about = "Two players alternate dropping discs into columns.\nFirst to connect four wins."
        tk.Label(f, text=about, font=textf, bg="#d0f0ea").pack(pady=(0, 15))
        tk.Label(f, text="How to Win:", font=labf, bg="#d0f0ea", anchor="w").pack(fill="x", padx=60)
        tips = "• Control center\n• Block opponent\n• Create forks"
        tk.Label(f, text=tips, font=textf, bg="#d0f0ea", justify="left").pack(fill="x", padx=80, pady=(0, 15))
        tk.Label(f, text="Game Devs: Tarun & Siddhartha", font=labf, bg="#d0f0ea").pack(pady=(0, 20))

        mf = tk.Frame(f, bg="#d0f0ea"); mf.pack(pady=5)
        tk.Label(mf, text="Mode:", font=labf, bg="#d0f0ea").grid(row=0, column=0, padx=5)
        self.mode = tk.StringVar(value="AI")
        for i, m in enumerate(("AI", "Hotseat")):
            tk.Radiobutton(mf, text=m, variable=self.mode, value=m, font=labf, bg="#d0f0ea")\
             .grid(row=0, column=i + 1, padx=10)

        df = tk.Frame(f, bg="#d0f0ea"); df.pack(pady=5)
        tk.Label(df, text="Difficulty:", font=labf, bg="#d0f0ea").grid(row=0, column=0, padx=5)
        self.diff = ttk.Combobox(df, values=list(DIFFICULTY), state="readonly", font=labf, width=8)
        self.diff.set("Medium"); self.diff.grid(row=0, column=1, padx=10)

        pf1 = tk.Frame(f, bg="#d0f0ea"); pf1.pack(fill="x", padx=60, pady=(15, 5))
        self.lbl1 = tk.Label(pf1, text="Player Name:", font=labf, bg="#d0f0ea")
        self.lbl1.grid(row=0, column=0, sticky="w")
        self.p1 = ttk.Entry(pf1, font=labf); self.p1.grid(row=0, column=1, sticky="we", padx=10)
        self.p1.insert(0, "Player"); pf1.columnconfigure(1, weight=1)

        pf2 = tk.Frame(f, bg="#d0f0ea")
        # pf2 not packed yet

        btn_frame = tk.Frame(f, bg="#d0f0ea")

        def toggle(*_):
            if self.mode.get() == "AI":
                self.lbl1.config(text="Player Name:")
                pf2.forget()
            else:
                self.lbl1.config(text="Player 1 Name:")
                pf2.pack(fill="x", padx=60, pady=(5, 15), before=btn_frame)

        self.mode.trace_add("write", toggle)
        toggle()

        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Start", font=btnf, bg="#457b9d", fg="white", width=10, command=self.start)\
          .pack(side="left", padx=10)
        tk.Button(btn_frame, text="Quit", font=btnf, bg="#e63946", fg="white", width=10, command=self.root.destroy)\
          .pack(side="left", padx=10)

        # now build pf2 inside landing
        tk.Label(pf2, text="Player 2 Name:", font=labf, bg="#d0f0ea")\
          .grid(row=0, column=0, sticky="w")
        self.p2 = ttk.Entry(pf2, font=labf); self.p2.grid(row=0, column=1, sticky="we", padx=10)
        self.p2.insert(0, "Player 2"); pf2.columnconfigure(1, weight=1)

    def _build_game(self):
        f = self.game = tk.Frame(self.root, bg="#d0f0ea")
        bar = tk.Frame(f, bg="#d0f0ea"); bar.pack(fill="x")
        tk.Button(bar, text="← Menu", font=("Segoe UI", 12), bg="#e63946", fg="white", command=self.back)\
          .pack(side="left", padx=10, pady=5)
        self.turn_lbl = tk.Label(bar, text="", font=("Segoe UI", 14), bg="#d0f0ea")
        self.turn_lbl.pack(side="left", padx=20)
        self.canvas = tk.Canvas(f, width=WIDTH, height=HEIGHT, bg="#164a86", highlightthickness=0)
        self.canvas.pack(padx=20, pady=10); self.canvas.bind("<Button-1>", self.click)

    def start(self):
        self.mode_sel = self.mode.get()
        self.depth = DIFFICULTY[self.diff.get()]
        self.player1 = self.p1.get().strip() or ("Player" if self.mode_sel == "AI" else "Player 1")
        self.player2 = "AI" if self.mode_sel == "AI" else (self.p2.get().strip() or "Player 2")
        self.landing.pack_forget(); self.game.pack(fill="both", expand=True)
        self.board = create_board(); self.turn = PLAYER; self.game_over = False
        self._draw_holes(); self.next_turn()

    def back(self):
        self.game.pack_forget(); self.landing.pack(fill="both", expand=True)

    def _draw_holes(self):
        self.canvas.delete("all")
        for r in range(ROWS):
            for c in range(COLS):
                x = c * SQUARE + SQUARE // 2; y = r * SQUARE + SQUARE // 2
                self.canvas.create_image(x, y, image=self.hole)

    def next_turn(self):
        if self.turn == PLAYER:
            name = ("Player" if self.mode_sel == "AI" else self.player1)
        else:
            name = ("AI"     if self.mode_sel == "AI" else self.player2)
        self.turn_lbl.config(text=f"{name}’s turn")
        if self.turn == AI and self.mode_sel == "AI":
            threading.Thread(target=self._ai_move, daemon=True).start()

    def _ai_move(self):
        time.sleep(0.3)
        col, _ = minimax(self.board, self.depth, -math.inf, math.inf, True)
        self.root.after(0, lambda:self.place(col))

    def click(self, e):
        if self.game_over: return
        if self.mode_sel == "AI" and self.turn != PLAYER: return
        col = e.x // SQUARE
        if 0 <= col < COLS and self.board[0][col] == EMPTY: self.place(col)

    def place(self, col):
        r = next_row(self.board, col); self.board[r][col] = self.turn
        x = col * SQUARE + SQUARE // 2; y = r * SQUARE + SQUARE // 2
        img = self.red if self.turn == PLAYER else self.yellow
        self.canvas.create_image(x, y, image=img)
        win = winning_line(self.board, self.turn)
        if win:
            self.game_over = True
            for rr, cc in win:
                x0, y0 = cc * SQUARE + 2, rr * SQUARE + 2
                x1, y1 = x0 + SQUARE - 4, y0 + SQUARE - 4
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="#FFD700", width=4)
            self._alert(f"{self.turn_lbl.cget('text')} wins!"); return
        if not valid_cols(self.board):
            self.game_over = True; self._alert("Draw!"); return
        if self.mode_sel == "AI":
            self.turn = AI if self.turn == PLAYER else PLAYER
        else:
            self.turn = AI if self.turn == PLAYER else PLAYER
        self.next_turn()

    def _alert(self, msg):
        d = tk.Toplevel(self.root); d.title("Game Over"); d.geometry("280x120")
        d.transient(self.root); d.grab_set()
        tk.Label(d, text=msg, font=("Segoe UI", 16, "bold")).pack(pady=10)
        bf = tk.Frame(d); bf.pack()
        tk.Button(bf, text="Again", command=lambda:[d.destroy(), self.start()]).pack(side="left", padx=5)
        tk.Button(bf, text="Quit", command=self.root.destroy).pack(side="left", padx=5)


if _name_ == "_main_":
    Connect4()