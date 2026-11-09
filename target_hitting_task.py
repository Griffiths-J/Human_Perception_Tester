import math
import random
import time
import tkinter as tk

import customtkinter as ctk

if __package__:
    from .data_logging import CSV_FILE, save_result
else:
    from data_logging import CSV_FILE, save_result


class TargetHittingTaskMixin:

    def start_fitts(self):

        self.fitts_trials = [
            (24, 120),
            (24, 240),
            (60, 120),
            (60, 240),
            (24, 120),
            (24, 240),
            (60, 120),
            (60, 240)
        ]

        random.shuffle(self.fitts_trials)

        self.fitts_trial_index = 0

        self.show_fitts_trial()


    def show_fitts_trial(self):

        self.clear_page()

        if self.fitts_trial_index >= len(self.fitts_trials):

            self.show_fitts_complete()

            return

        self.fitts_size, self.fitts_distance = (
            self.fitts_trials[self.fitts_trial_index]
        )

        trial_number = self.fitts_trial_index + 1

        self.title_block(
            f"Target Hitting Task — Trial {trial_number} of 8",
            "Click the START marker first, then click the target."
        )

        ctk.CTkLabel(
            self.current_frame,
            text=f"Target size: {self.fitts_size}px     "
                 f"Distance: {self.fitts_distance}px",
            font=("Arial", 14, "bold")
        ).pack(pady=3)

        background, text_color, target_color = (
            self.get_visual_colors()
        )

        self.fitts_canvas = tk.Canvas(
            self.current_frame,
            width=760,
            height=430,
            bg=background,
            highlightthickness=1,
            highlightbackground="#888888"
        )

        self.fitts_canvas.pack(pady=10)

        self.start_x = 380
        self.start_y = 215

        valid_angles = [
            0, 30, 150, 180, 210, 330
        ]

        angle = math.radians(
            random.choice(valid_angles)
        )

        self.target_x = (
            self.start_x
            + self.fitts_distance * math.cos(angle)
        )

        self.target_y = (
            self.start_y
            + self.fitts_distance * math.sin(angle)
        )

        self.target_radius = self.fitts_size / 2

        self.fitts_canvas.create_oval(
            self.start_x - 12,
            self.start_y - 12,
            self.start_x + 12,
            self.start_y + 12,
            fill=text_color,
            outline=text_color
        )

        self.fitts_canvas.create_text(
            self.start_x,
            self.start_y + 25,
            text="START",
            fill=text_color,
            font=("Arial", 11, "bold")
        )

        self.fitts_canvas.create_oval(
            self.target_x - self.target_radius,
            self.target_y - self.target_radius,
            self.target_x + self.target_radius,
            self.target_y + self.target_radius,
            fill=target_color,
            outline=text_color,
            width=2
        )

        self.fitts_status = ctk.CTkLabel(
            self.current_frame,
            text="Click the START marker to begin."
        )

        self.fitts_status.pack(pady=3)

        self.fitts_rating = self.rating_control(
            self.current_frame
        )

        self.fitts_rating.configure(
            state="disabled"
        )

        self.fitts_started = False

        self.fitts_elapsed = None

        self.fitts_canvas.bind(
            "<Button-1>",
            self.handle_fitts_click
        )

        ctk.CTkButton(
            self.current_frame,
            text="Cancel / Back to Dashboard",
            fg_color="gray",
            command=self.show_dashboard
        ).pack(pady=5)


    def handle_fitts_click(self, event):

        start_dx = event.x - self.start_x

        start_dy = event.y - self.start_y

        start_distance = math.sqrt(
            start_dx ** 2 + start_dy ** 2
        )

        target_dx = event.x - self.target_x

        target_dy = event.y - self.target_y

        target_distance = math.sqrt(
            target_dx ** 2 + target_dy ** 2
        )

        if not self.fitts_started:

            if start_distance <= 18:

                self.fitts_started = True

                self.fitts_start_time = time.perf_counter()

                self.fitts_status.configure(
                    text="Timing started! Click the target."
                )

            else:

                self.fitts_status.configure(
                    text="Please click the START marker first."
                )

            return

        if target_distance <= self.target_radius:

            self.fitts_elapsed = (
                time.perf_counter()
                - self.fitts_start_time
            )

            self.fitts_status.configure(
                text=f"Target hit! Movement time: "
                     f"{self.fitts_elapsed:.3f} seconds. "
                     f"Rate the ease of use."
            )

            self.fitts_rating.configure(
                state="normal"
            )

            self.fitts_canvas.unbind(
                "<Button-1>"
            )

            self.fitts_canvas.create_text(
                380,
                25,
                text="TARGET HIT",
                fill="#16803C",
                font=("Arial", 15, "bold")
            )

            ctk.CTkButton(
                self.current_frame,
                text="Save Rating & Next Trial",
                width=230,
                command=self.save_fitts_trial
            ).pack(pady=5)

        else:

            self.fitts_status.configure(
                text="You missed the target. Try clicking inside it."
            )


    def save_fitts_trial(self):

        result = self.create_result(
            task="Target Hitting",
            elapsed=self.fitts_elapsed,
            rating=self.fitts_rating.get(),
            target_size=self.fitts_size,
            distance=self.fitts_distance,
            trial=self.fitts_trial_index + 1
        )

        save_result(result)

        self.fitts_trial_index += 1

        self.show_fitts_trial()


    def show_fitts_complete(self):

        self.clear_page()

        self.title_block(
            "Target Hitting Task Complete",
            "All eight trials have been completed."
        )

        ctk.CTkLabel(
            self.current_frame,
            text=f"Your results have been saved in {CSV_FILE.name}.",
            font=("Arial", 15)
        ).pack(pady=20)

        ctk.CTkLabel(
            self.current_frame,
            text="You can repeat the experiment with another participant.",
            font=("Arial", 13)
        ).pack(pady=5)

        ctk.CTkButton(
            self.current_frame,
            text="Back to Dashboard",
            command=self.show_dashboard,
            width=190
        ).pack(pady=15)
