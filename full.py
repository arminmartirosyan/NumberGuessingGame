import customtkinter as ctk
from tkinter import messagebox
import random
import json
import os
import time

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class NumberGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("GUESS THE NUMBER")
        self.root.geometry("550x500")
        self.root.resizable(False, False)

        self.score_file = "scores.json"

        self.difficulty_ranges = {
            "Easy": 50,
            "Medium": 100,
            "Hard": 500
        }

        self.current_difficulty = "Medium"

        self.target_number = 0
        self.guess_count = 0
        self.start_time = 0

        self.create_ui()
        self.reset_game()

    def create_ui(self):

        self.title_label = ctk.CTkLabel(
            self.root,
            text="AI NUMBER HUNTER",
            font=("Arial", 28, "bold")
        )
        self.title_label.pack(pady=20)

        self.subtitle_label = ctk.CTkLabel(
            self.root,
            text="Try to crack the hidden number",
            font=("Arial", 14)
        )
        self.subtitle_label.pack(pady=5)

        # Difficulty Menu
        self.difficulty_menu = ctk.CTkOptionMenu(
            self.root,
            values=["Easy", "Medium", "Hard"],
            command=self.change_difficulty
        )
        self.difficulty_menu.set("Medium")
        self.difficulty_menu.pack(pady=15)

        # Entry
        self.entry = ctk.CTkEntry(
            self.root,
            placeholder_text="Enter your guess...",
            width=250,
            height=40,
            font=("Arial", 16),
            justify="center"
        )
        self.entry.pack(pady=10)

        # Submit Button
        self.submit_button = ctk.CTkButton(
            self.root,
            text="Submit Guess",
            command=self.check_guess,
            width=200,
            height=40,
            font=("Arial", 15, "bold")
        )
        self.submit_button.pack(pady=10)

        # Hint Button
        self.hint_button = ctk.CTkButton(
            self.root,
            text="Get Hint",
            command=self.show_hint,
            width=200,
            height=40
        )
        self.hint_button.pack(pady=5)

        # Reset Button
        self.reset_button = ctk.CTkButton(
            self.root,
            text="Reset Game",
            command=self.reset_game,
            fg_color="#d9534f",
            hover_color="#c9302c",
            width=200,
            height=40
        )
        self.reset_button.pack(pady=10)

        # Feedback Box
        self.feedback_label = ctk.CTkLabel(
            self.root,
            text="",
            width=400,
            height=80,
            corner_radius=15,
            font=("Arial", 18, "bold")
        )
        self.feedback_label.pack(pady=25)

        # Stats
        self.stats_label = ctk.CTkLabel(
            self.root,
            text="Attempts: 0 | Time: 0s",
            font=("Arial", 14)
        )
        self.stats_label.pack(pady=5)

        # Leaderboard
        self.leaderboard_label = ctk.CTkLabel(
            self.root,
            text="🏆 Best Score: None",
            font=("Arial", 14, "bold")
        )
        self.leaderboard_label.pack(pady=15)

        self.load_best_score()

    def change_difficulty(self, difficulty):
        self.current_difficulty = difficulty
        self.reset_game()

    def reset_game(self):
        max_number = self.difficulty_ranges[self.current_difficulty]

        self.target_number = random.randint(1, max_number)
        self.guess_count = 0
        self.start_time = time.time()

        self.entry.delete(0, "end")

        self.feedback_label.configure(
            text=f"Guess a number between 1 and {max_number}",
            text_color="white"
        )

        self.stats_label.configure(
            text="Attempts: 0 | Time: 0s"
        )

    def check_guess(self):

        user_input = self.entry.get()

        if not user_input.isdigit():
            self.feedback_label.configure(
                text="Invalid input! Enter a valid number.",
                text_color="red"
            )
            return

        guess = int(user_input)

        self.guess_count += 1

        elapsed_time = int(time.time() - self.start_time)

        self.stats_label.configure(
            text=f"Attempts: {self.guess_count} | Time: {elapsed_time}s"
        )

        if guess < self.target_number:

            self.feedback_label.configure(
                text="Too Low!",
                text_color="#4da6ff"
            )

        elif guess > self.target_number:

            self.feedback_label.configure(
                text="Too High!",
                text_color="#ffb84d"
            )

        else:

            score = self.calculate_score(elapsed_time)

            self.feedback_label.configure(
                text=f"Correct! Score: {score}",
                text_color="#00ff99"
            )

            self.save_best_score(score)

            messagebox.showinfo(
                "Victory",
                f"You guessed the number in {self.guess_count} attempts.\n"
                f"Time: {elapsed_time} seconds\n"
                f"Score: {score}"
            )

            self.reset_game()

    def calculate_score(self, elapsed_time):

        base_score = 1000

        penalty_attempts = self.guess_count * 25
        penalty_time = elapsed_time * 2

        return max(0, base_score - penalty_attempts - penalty_time)

    def show_hint(self):

        if self.target_number % 2 == 0:
            hint = "The number is EVEN."
        else:
            hint = "The number is ODD."

        self.feedback_label.configure(
            text=hint,
            text_color="#00ccff"
        )

    def save_best_score(self, score):

        best_score = 0

        if os.path.exists(self.score_file):

            with open(self.score_file, "r") as file:
                data = json.load(file)
                best_score = data.get("best_score", 0)

        if score > best_score:

            with open(self.score_file, "w") as file:
                json.dump({"best_score": score}, file)

        self.load_best_score()

    def load_best_score(self):

        if os.path.exists(self.score_file):

            with open(self.score_file, "r") as file:
                data = json.load(file)

                best_score = data.get("best_score", 0)

                self.leaderboard_label.configure(
                    text=f"🏆 Best Score: {best_score}"
                )

        else:
            self.leaderboard_label.configure(
                text="🏆 Best Score: None"
            )


if __name__ == "__main__":

    root = ctk.CTk()

    app = NumberGuessingGame(root)

    root.mainloop()